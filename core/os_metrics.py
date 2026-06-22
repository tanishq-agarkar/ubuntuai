
import os, time, subprocess

def _read(path):

    try:

        with open(path) as f: return f.read()

    except: return ""

def memory_info():

    lines = _read("/proc/meminfo").splitlines()

    data = {l.split()[0].rstrip(":"): int(l.split()[1]) for l in lines if len(l.split()) >= 2}

    total = data.get("MemTotal", 0)

    avail = data.get("MemAvailable", 0)

    return {"total_mb": total//1024, "available_mb": avail//1024, "percent_used": round((total-avail)/total*100,1) if total else 0}

def cpu_info():

    with open("/proc/stat") as f: l1 = f.readline().split()[1:]

    time.sleep(0.2)

    with open("/proc/stat") as f: l2 = f.readline().split()[1:]

    n1, n2 = list(map(int, l1)), list(map(int, l2))

    dt = sum(n2) - sum(n1)

    return {"percent_used": round((1 - (n2[3]-n1[3])/dt)*100,1) if dt else 0.0}

def disk_info():

    try:

        out = subprocess.check_output(["df","-h"], text=True)

        return [{"device":p[0],"size":p[1],"avail":p[3],"mount":p[5]} for p in [line.split() for line in out.splitlines()[1:]] if len(p) >= 6 and "tmpfs" not in p[0]]

    except: return []

def fast_snapshot():

    mem = memory_info()

    return {"ram_available_mb": mem["available_mb"], "ram_total_mb": mem["total_mb"]}

def full_snapshot():

    return {"memory": memory_info(), "cpu": cpu_info(), "disk": disk_info()}

