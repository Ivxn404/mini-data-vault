import random
import hashlib
import csv
import os
from datetime import datetime

# Policy Database with versioning
POLICY_DB = {
    "device_alpha": {
        "v": "1.2.4",
        "rules": {
            "cpu_usage": "share_if_above_85",
            "disk_usage": "always_share",
            "memory_usage": "share_if_above_90",
            "network_activity": "share_if_role_admin",
            "gps_location": "do_not_share",
            "sensor_status": "share_if_alert",
            "uptime_hours": "always_share",
            "log_entry": "share_if_pattern_error",
        },
        "override_on_alert": True
    },
    "device_beta": {
        "v": "1.0.9",
        "rules": {
            "cpu_usage": "do_not_share",
            "disk_usage": "share_if_above_70",
            "memory_usage": "do_not_share",
            "network_activity": "do_not_share",
            "gps_location": "do_not_share",
            "sensor_status": "share_if_alert",
            "uptime_hours": "always_share",
            "log_entry": "do_not_share",
        },
        "override_on_alert": False
    }
}

# Device registry
DEVICES = {
    "device_alpha": {"user": "admin_node", "role": "admin", "trust_score": 0},
    "device_beta": {"user": "ops_node", "role": "technician", "trust_score": 0}
}

# Simulate IoT data
def simulate_data():
    return {
        "cpu_usage": round(random.uniform(10, 100), 2),
        "disk_usage": round(random.uniform(30, 100), 2),
        "memory_usage": round(random.uniform(40, 100), 2),
        "network_activity": f"{random.randint(100, 8000)} KB/s",
        "gps_location": "19.07°N, 72.87°E",
        "sensor_status": random.choice(["OK", "Overheat", "Motion", "Critical"]),
        "uptime_hours": random.randint(1, 5000),
        "log_entry": random.choice([
            "INFO: Boot complete",
            "WARN: Temp spike",
            "ERROR: Failed handshake",
            "DEBUG: Maintenance mode"
        ])
    }

# Encrypt a value
def encrypt(value):
    return hashlib.sha256(str(value).encode()).hexdigest()

# Classify each data field by retention tag
def classify_tag(field):
    if field in ["cpu_usage", "memory_usage"]:
        return "critical"
    elif field in ["gps_location", "network_activity"]:
        return "transient"
    elif field in ["log_entry", "sensor_status"]:
        return "diagnostic"
    return "archive"

# Apply policy to a device's telemetry data
def apply_policy(data, policy_set, user):
    filtered = {}
    violations = []
    tags = []
    rule_set = policy_set["rules"]
    override = policy_set.get("override_on_alert", False)
    alert_triggered = data.get("sensor_status") in ["Critical", "Overheat", "Motion"]

    for field, value in data.items():
        rule = rule_set.get(field, "do_not_share")
        tag = classify_tag(field)
        tags.append(tag)

        if override and alert_triggered:
            filtered[field] = encrypt(value)
            continue

        try:
            if rule == "always_share":
                filtered[field] = encrypt(value)
            elif rule == "do_not_share":
                continue
            elif rule == "share_if_above_85" and float(value) > 85:
                filtered[field] = encrypt(value)
            elif rule == "share_if_above_90" and float(value) > 90:
                filtered[field] = encrypt(value)
            elif rule == "share_if_above_70" and float(value) > 70:
                filtered[field] = encrypt(value)
            elif rule == "share_if_role_admin" and user["role"] == "admin":
                filtered[field] = encrypt(value)
            elif rule == "share_if_alert" and str(value) in ["Overheat", "Motion", "Critical"]:
                filtered[field] = encrypt(value)
            elif rule == "share_if_pattern_error" and "ERROR" in str(value).upper():
                filtered[field] = encrypt(value)
        except Exception:
            violations.append((field, value, rule))

    return filtered, violations, tags

# CSV logger
def log_to_csv(filename, header, row):
    write_header = not os.path.exists(filename)
    with open(filename, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

# Log policy violations
def log_violation(device_id, violations):
    for field, value, rule in violations:
        row = {
            "timestamp": datetime.now().isoformat(),
            "device_id": device_id,
            "field": field,
            "value": value,
            "policy_rule": rule,
            "violation_type": "PolicyMismatch"
        }
        log_to_csv("policy_violation_log.csv", row.keys(), row)

# Log cloud upload (encrypted)
def log_cloud_upload(device_id, encrypted_data):
    row = {
        "timestamp": datetime.now().isoformat(),
        "device_id": device_id
    }
    row.update(encrypted_data)
    log_to_csv("cloud_storage.csv", row.keys(), row)

# Log activity + tags
def log_audit(device_id, fields, tags, cycle, alert_flag):
    row = {
        "timestamp": datetime.now().isoformat(),
        "device_id": device_id,
        "fields_shared": ", ".join(fields),
        "count": len(fields),
        "tags": ", ".join(set(tags)),
        "alert_override": alert_flag,
        "cycle_id": cycle
    }
    log_to_csv("upload_log.csv", row.keys(), row)

# Trust score computation
def trust_score_update(device_id, shared_fields):
    score_file = "trust_score_log.csv"
    trust_boost = len(shared_fields) * 2
    DEVICES[device_id]["trust_score"] += trust_boost

    row = {
        "timestamp": datetime.now().isoformat(),
        "device_id": device_id,
        "score_delta": trust_boost,
        "current_score": DEVICES[device_id]["trust_score"]
    }
    log_to_csv(score_file, row.keys(), row)

# Simulation Engine
def simulate_cycle(cycle_id=1):
    for device_id, user in DEVICES.items():
        print(f"\n[Cycle {cycle_id}] Processing {device_id} ({user['role']})")

        raw_data = simulate_data()
        print("Raw:", raw_data)

        policy_set = POLICY_DB.get(device_id)
        if not policy_set:
            print("No policy assigned.")
            continue

        filtered, violations, tags = apply_policy(raw_data, policy_set, user)
        print("Shared:", filtered)

        if filtered:
            log_cloud_upload(device_id, filtered)
            log_audit(device_id, list(filtered.keys()), tags, cycle_id, policy_set.get("override_on_alert", False))
            trust_score_update(device_id, filtered)
        if violations:
            log_violation(device_id, violations)

# Run Simulation
for i in range(1, 4):  # Simulate 3 cycles
    simulate_cycle(cycle_id=i)

print("\nSimulation complete. Output written to:")
print("- cloud_storage.csv")
print("- upload_log.csv")
print("- trust_score_log.csv")
print("- policy_violation_log.csv")
