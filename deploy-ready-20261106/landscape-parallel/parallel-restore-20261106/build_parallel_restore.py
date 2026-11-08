# -*- coding: utf-8 -*-
from __future__ import annotations
import json, re, sqlite3, shutil, hashlib
from pathlib import Path

WORK = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel\parallel-restore-20261106")
RULES = json.loads((WORK / "native-window-rules.json").read_text(encoding="utf-8"))
INSTALLED = set(Path(WORK / "installed-packages.txt").read_text(encoding="utf-8").splitlines()) if (WORK / "installed-packages.txt").exists() else set()

def md5(p: Path) -> str:
    h = hashlib.md5(); h.update(p.read_bytes()); return h.hexdigest()

def esc_body(obj) -> str:
    # OEM fantasy XML uses ^ as quote stand-in inside attribute
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace('"', "^")

def patch_xml_attr(xml: str, tag: str, pkg: str, updates: dict) -> tuple[str, int]:
    """Update attributes on <tag package_name="pkg" ...> element (self-closing or open)."""
    pat = re.compile(
        rf'(<{tag}\b(?=[^>]*\bpackage_name="{re.escape(pkg)}")[^>]*?)(/?>)',
        re.S,
    )
    n = 0
    def repl(m):
        nonlocal n
        head, end = m.group(1), m.group(2)
        for k, v in updates.items():
            if re.search(rf'\b{k}="', head):
                head = re.sub(rf'\b{k}="[^"]*"', f'{k}="{v}"', head, count=1)
            else:
                head = head.rstrip() + f' {k}="{v}"'
        n += 1
        return head + end
    out = pat.sub(repl, xml)
    return out, n

def bump_version(xml: str, at_least: int) -> str:
    m = re.search(r"<version>(\d+)</version>", xml)
    assert m, "no version"
    ver = max(int(m.group(1)) + 1, at_least)
    return re.sub(r"<version>\d+</version>", f"<version>{ver}</version>", xml, count=1)

def main():
    assert INSTALLED, "need installed-packages.txt"
    db_src = WORK / "fantasywindow.base.db"
    db_out = WORK / "fantasywindow.parallel-v1.db"
    shutil.copy2(db_src, db_out)
    con = sqlite3.connect(str(db_out))
    cur = con.cursor()

    # All magic packages present on device
    cur.execute("SELECT package_name, status, config, custom_config_body FROM t_config WHERE use_function='magicwindow'")
    magic_rows = cur.fetchall()
    on_device_magic = [(p,s,c,b) for (p,s,c,b) in magic_rows if p in INSTALLED]

    # Pre-bulk FO bodies for restore (from XML)
    pre_fo = (WORK / "sys_fo.pre-bulk.xml").read_text(encoding="utf-8")
    pre_fo_map = {}
    for m in re.finditer(r'<o\b[^>]*package_name="([^"]+)"[^>]*status="([^"]+)"[^>]*custom_config_body="([^"]*)"[^>]*/>', pre_fo):
        pkg, st, body = m.group(1), m.group(2), m.group(3).replace("^", '"')
        pre_fo_map[pkg] = (st, body)

    stats = {
        "on_device_magic": len(on_device_magic),
        "magic_enabled": 0,
        "magic_exclude_stripped": 0,
        "fo_to_status2": 0,
        "wechat_scale": 0,
        "qq_douyin_magic_on": 0,
        "db_fo_updated": 0,
        "db_magic_updated": 0,
    }

    wechat_magic_body = RULES["sys_fantasy_window_managed"]["apps"]["com.tencent.mm"]
    wechat_fo_body = RULES["sys_full_orientation_managed"]["apps"]["com.tencent.mm"]
    bili_magic = RULES["sys_fantasy_window_managed"]["apps"].get("tv.danmaku.bili")
    bili_fo = RULES["sys_full_orientation_managed"]["apps"].get("tv.danmaku.bili")

    force_magic_on = {"com.tencent.mobileqq", "com.ss.android.ugc.aweme", "com.tencent.mm"}
    if "tv.danmaku.bili" in INSTALLED:
        force_magic_on.add("tv.danmaku.bili")

    for pkg, status, config, custom in on_device_magic:
        new_status = 1
        new_config = config or ""
        new_custom = custom or ""
        # strip excludeDevice PAD from config JSON if present
        if new_config and "excludeDevice" in new_config:
            try:
                obj = json.loads(new_config)
                if str(obj.get("excludeDevice", "")).upper() == "PAD" or "PAD" in str(obj.get("excludeDevice", "")):
                    obj.pop("excludeDevice", None)
                    new_config = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
                    stats["magic_exclude_stripped"] += 1
            except Exception:
                new_config = re.sub(r',"excludeDevice":"[^"]*"', "", new_config)
                new_config = re.sub(r'"excludeDevice":"[^"]*",?', "", new_config)
                stats["magic_exclude_stripped"] += 1
        if pkg == "com.tencent.mm":
            # merge scaleWindow=-1 + isDraggable into custom_config_body
            try:
                cobj = json.loads(new_custom) if new_custom else {}
            except Exception:
                cobj = {}
            cobj["scaleWindow"] = "-1"
            cobj.setdefault("noRelaunchOnResize", "true")
            ux = cobj.get("UX") or {}
            ux["isDraggable"] = "true"
            # keep/override PAD ratio from rules if present
            if "windowsRatio" in wechat_magic_body.get("UX", {}):
                ux["windowsRatio"] = wechat_magic_body["UX"]["windowsRatio"]
            cobj["UX"] = ux
            # prefer Activities from rules
            if "Activities" in wechat_magic_body:
                cobj["Activities"] = wechat_magic_body["Activities"]
            new_custom = json.dumps(cobj, ensure_ascii=False, separators=(",", ":"))
            stats["wechat_scale"] += 1
        if pkg == "tv.danmaku.bili" and bili_magic:
            try:
                cobj = json.loads(new_custom) if new_custom else {}
            except Exception:
                cobj = {}
            cobj["scaleWindow"] = "-1"
            cobj["noRelaunchOnResize"] = "true"
            cobj["blockSensor"] = "true"
            cobj["adjustDisplayRotation"] = "0"
            if "Activities" in bili_magic:
                cobj["Activities"] = bili_magic["Activities"]
            if "UX" in bili_magic:
                cobj["UX"] = bili_magic["UX"]
            new_custom = json.dumps(cobj, ensure_ascii=False, separators=(",", ":"))
        if int(status) != 1 or new_config != (config or "") or new_custom != (custom or ""):
            cur.execute(
                "UPDATE t_config SET status=?, config=?, custom_config_body=?, installed=1 WHERE package_name=? AND use_function='magicwindow'",
                (new_status, new_config, new_custom, pkg),
            )
            stats["db_magic_updated"] += 1
        else:
            cur.execute(
                "UPDATE t_config SET installed=1 WHERE package_name=? AND use_function='magicwindow'",
                (pkg,),
            )
        stats["magic_enabled"] += 1
        if pkg in ("com.tencent.mobileqq", "com.ss.android.ugc.aweme"):
            stats["qq_douyin_magic_on"] += 1

        # FO: demote to status=2 so magic dual-pane wins
        fo_status, fo_body = "2", json.dumps({"rao": "false", "rotate_cam": "false"}, separators=(",", ":"))
        if pkg == "com.tencent.mm":
            fo_body = json.dumps(wechat_fo_body, ensure_ascii=False, separators=(",", ":"))
        elif pkg == "tv.danmaku.bili" and bili_fo:
            fo_body = json.dumps(bili_fo, ensure_ascii=False, separators=(",", ":"))
        elif pkg in pre_fo_map and pre_fo_map[pkg][0] == "2":
            fo_status, fo_body = pre_fo_map[pkg][0], pre_fo_map[pkg][1]
        # QQ/Douyin: FO off for parallel primary
        if pkg in ("com.tencent.mobileqq", "com.ss.android.ugc.aweme"):
            fo_status, fo_body = "2", json.dumps({"rao": "false", "rotate_cam": "false"}, separators=(",", ":"))

        cur.execute("SELECT 1 FROM t_config WHERE package_name=? AND use_function='fullorientation'", (pkg,))
        if cur.fetchone():
            cur.execute(
                "UPDATE t_config SET status=?, config=?, custom_config_body=? WHERE package_name=? AND use_function='fullorientation'",
                (int(fo_status), fo_body, fo_body, pkg),
            )
        else:
            cur.execute(
                "INSERT INTO t_config(package_name, use_function, config, data_sources, status, custom_mode, custom_config_body, func_version, installed) VALUES (?,?,?,?,?,?,?,?,?)",
                (pkg, "fullorientation", fo_body, 1, int(fo_status), -1, fo_body, "", 1),
            )
        stats["db_fo_updated"] += 1
        stats["fo_to_status2"] += 1

    con.commit()

    # counts
    cur.execute("SELECT status, COUNT(*) FROM t_config WHERE use_function='magicwindow' AND installed=1 GROUP BY status")
    stats["db_magic_installed_status"] = cur.fetchall()
    cur.execute(
        "SELECT package_name, status FROM t_config WHERE use_function='magicwindow' AND package_name IN ('com.tencent.mm','com.tencent.mobileqq','com.ss.android.ugc.aweme','tv.danmaku.bili')"
    )
    stats["key_magic"] = cur.fetchall()
    cur.execute(
        "SELECT package_name, status, substr(custom_config_body,1,80) FROM t_config WHERE use_function='fullorientation' AND package_name IN ('com.tencent.mm','com.tencent.mobileqq','com.ss.android.ugc.aweme','tv.danmaku.bili')"
    )
    stats["key_fo"] = cur.fetchall()
    con.close()

    # --- Product XMLs ---
    fo_xml = (WORK / "sys_fo.base.xml").read_text(encoding="utf-8")
    fw_xml = (WORK / "sys_fantasy_window_managed.base.xml").read_text(encoding="utf-8")

    for pkg, status, config, custom in on_device_magic:
        # magic product: status=1, update custom for wechat/bili/qq/douyin
        updates = {"status": "1"}
        if pkg == "com.tencent.mm":
            updates["custom_config_body"] = esc_body(wechat_magic_body)
        elif pkg == "tv.danmaku.bili" and bili_magic:
            updates["custom_config_body"] = esc_body(bili_magic)
        elif pkg in ("com.tencent.mobileqq", "com.ss.android.ugc.aweme"):
            # keep existing body but ensure status 1; strip forceBlock if any via regex later
            pass
        fw_xml, n = patch_xml_attr(fw_xml, "a", pkg, updates)
        if n == 0:
            stats.setdefault("fw_xml_miss", []).append(pkg)

        fo_status = "2"
        if pkg == "com.tencent.mm":
            body = esc_body(wechat_fo_body)
        elif pkg == "tv.danmaku.bili" and bili_fo:
            body = esc_body(bili_fo)
        else:
            body = esc_body({"rao": "false", "rotate_cam": "false"})
        fo_xml, n = patch_xml_attr(fo_xml, "o", pkg, {"status": fo_status, "custom_config_body": body})
        if n == 0:
            stats.setdefault("fo_xml_miss", []).append(pkg)

    # Explicit strip forceBlock / ensure QQ douyin product magic status
    for pkg in ("com.tencent.mobileqq", "com.ss.android.ugc.aweme"):
        fw_xml, _ = patch_xml_attr(fw_xml, "a", pkg, {"status": "1"})
        # remove forceBlock from custom if present in attribute text
        fw_xml = re.sub(
            rf'(<a\b[^>]*package_name="{pkg}"[^>]*custom_config_body="[^"]*)\^forceBlock\^:\^true\^(,?)',
            lambda m: m.group(1) + ("" if not m.group(2) else ""),
            fw_xml,
        )

    fo_xml = bump_version(fo_xml, int(RULES["sys_full_orientation_managed"]["version"]))
    fw_xml = bump_version(fw_xml, int(RULES["sys_fantasy_window_managed"]["version"]))

    fo_out = WORK / "sys_full_orientation_managed.parallel-v1.xml"
    fw_out = WORK / "sys_fantasy_window_managed.parallel-v1.xml"
    fo_out.write_text(fo_xml, encoding="utf-8", newline="\n")
    fw_out.write_text(fw_xml, encoding="utf-8", newline="\n")

    report = {
        "stats": stats,
        "md5": {
            "db": md5(db_out),
            "fo": md5(fo_out),
            "fw": md5(fw_out),
            "fo_base": md5(WORK / "sys_fo.base.xml"),
            "fw_base": md5(WORK / "sys_fantasy_window_managed.base.xml"),
        },
        "key_checks": {
            "fo_wechat": re.search(r'package_name="com.tencent.mm"[^>]*status="(\d)"', fo_xml).group(1) if re.search(r'package_name="com.tencent.mm"[^>]*status="(\d)"', fo_xml) else None,
            "fw_wechat": re.search(r'package_name="com.tencent.mm"[^>]*status="(\d)"', fw_xml).group(1) if re.search(r'package_name="com.tencent.mm"[^>]*status="(\d)"', fw_xml) else None,
            "fw_qq": re.search(r'package_name="com.tencent.mobileqq"[^>]*status="(\d)"', fw_xml).group(1) if re.search(r'package_name="com.tencent.mobileqq"[^>]*status="(\d)"', fw_xml) else None,
            "fw_aweme": re.search(r'package_name="com.ss.android.ugc.aweme"[^>]*status="(\d)"', fw_xml).group(1) if re.search(r'package_name="com.ss.android.ugc.aweme"[^>]*status="(\d)"', fw_xml) else None,
        },
    }
    (WORK / "bake-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
