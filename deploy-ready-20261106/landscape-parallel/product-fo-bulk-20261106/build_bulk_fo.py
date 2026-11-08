# -*- coding: utf-8 -*-
"""Bulk FO product bake + runtime DB sync for TB371FC ColorOS16.
Policy: native fullorientation (rao:true), NOT magic-as-landscape.
"""
from __future__ import annotations
import hashlib, json, re, shutil, sqlite3
from pathlib import Path
from collections import Counter

BASE = Path(r"D:\TB371FC-release\clean-rebase-20261104\deploy-ready-20261106\landscape-parallel")
OUT = BASE / "product-fo-bulk-20261106"
PROBE = BASE / "probe"
OUT.mkdir(parents=True, exist_ok=True)

LIVE_FO = PROBE / "sys_full_orientation_managed.live.xml"
LIVE_FW = PROBE / "sys_fantasy_window_managed.live.xml"
LIVE_DB = PROBE / "fw-bulk.db"
PKGS3 = PROBE / "pkgs-user3.txt"

SAFE_BODY_CARET = "{^rao^:^true^,^rotate_cam^:^false^}"
SAFE_BODY_JSON = '{"rao":"true","rotate_cam":"false"}'

# Keep FO off for these (banks / payment / sensitive) even if status=0
FO_OFF_DENY = {
    "cmb.pb", "com.android.bankabc", "com.chinamworld.main", "com.icbc",
    "com.eg.android.AlipayGphone", "com.unionpay", "com.hexin.plat.android",
    "com.ebank.creditcard", "com.chinamworld.bocmbci", "com.yitong.mbank.psbc",
    "com.bankcomm.Bankcomm", "com.cmbchina.ccd.pluto.cmbActivity",
    "com.android.icbc", "cn.com.cmbc.newmbank", "com.pingan.banks",
    "com.tenpay.android", "com.tencent.weread",  # keep weread? actually reading wants landscape - remove
}
FO_OFF_DENY.discard("com.tencent.weread")

# Installed / present packages to ADD if missing from FO XML
ADD_FO_PKGS = [
    "com.heytap.yoli",
    "com.heytap.music",
    "com.heytap.reader",
    "com.heytap.browser",
    "com.coloros.video",
    "com.coloros.gallery3d",
    "andes.oplus.documentsreader",
]

# Parallel magic: add conservative dual-pane for installed apps missing from fantasy list
# (NOT used as landscape substitute; FO remains primary for land)
ADD_MAGIC_PKGS = [
    "com.heytap.yoli",
    "com.heytap.music",
    "com.heytap.reader",
    "com.heytap.browser",
    "com.coloros.video",
    "com.coloros.gallery3d",
    "andes.oplus.documentsreader",
]
MAGIC_TMPL = (
    '<a package_name="{pkg}" status="1" use_function="magicwindow" '
    'custom_config_body="{{^force_custom_pw_mode^:^true^,^mode^:^1^,^fullOrientation^:^true^,'
    '^activityPairs^:[{{^from^:^MainActivity^,^to^:^*^}}],^noRelaunchOnResize^:^true^,'
    '^adjustDisplayRotation^:^0^,^blockSensor^:^true^,^scaleWindow^:^-1^}}" />'
)

def md5_bytes(b: bytes) -> str:
    return hashlib.md5(b).hexdigest()

def md5_text(t: str) -> str:
    return md5_bytes(t.encode("utf-8"))

def load_pkgs3():
    pkgs = []
    for ln in PKGS3.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if ln.startswith("package:"):
            pkgs.append(ln.split(":", 1)[1].strip())
    return pkgs

def transform_fo(xml: str):
    stats = Counter()
    # Match each <o ... /> entry
    pat = re.compile(r'<o\s+([^>]+?)\s*/>')

    def repl(m: re.Match) -> str:
        attrs = m.group(1)
        pkg_m = re.search(r'package_name="([^"]+)"', attrs)
        st_m = re.search(r'status="(\d)"', attrs)
        body_m = re.search(r'custom_config_body="([^"]*)"', attrs)
        if not pkg_m or not st_m:
            return m.group(0)
        pkg, st = pkg_m.group(1), st_m.group(1)
        body = body_m.group(1) if body_m else ""

        # Preserve rotate_cam true if present
        rotate_cam = "true" if "^rotate_cam^:^true^" in body or '"rotate_cam":"true"' in body else "false"
        new_body = "{^rao^:^true^,^rotate_cam^:^%s^}" % rotate_cam

        if pkg in FO_OFF_DENY:
            stats["deny_kept"] += 1
            if st != "0":
                attrs2 = re.sub(r'status="\d"', 'status="0"', attrs, count=1)
                attrs2 = re.sub(r'custom_config_body="[^"]*"', f'custom_config_body="{SAFE_BODY_CARET}"', attrs2, count=1)
                stats["deny_forced_off"] += 1
                return f"<o {attrs2} />"
            return m.group(0)

        if st == "2":
            stats["status2_to_1"] += 1
            attrs2 = re.sub(r'status="\d"', 'status="1"', attrs, count=1)
            attrs2 = re.sub(r'custom_config_body="[^"]*"', f'custom_config_body="{new_body}"', attrs2, count=1)
            return f"<o {attrs2} />"

        if st == "0":
            # bulk enable non-deny
            stats["status0_to_1"] += 1
            attrs2 = re.sub(r'status="\d"', 'status="1"', attrs, count=1)
            attrs2 = re.sub(r'custom_config_body="[^"]*"', f'custom_config_body="{new_body}"', attrs2, count=1)
            return f"<o {attrs2} />"

        if st == "1":
            # simplify trap bodies even when already status=1
            if "alwaysFullOrientActivities" in body or "orientForStarting" in body:
                stats["status1_trap_simplified"] += 1
                attrs2 = re.sub(r'custom_config_body="[^"]*"', f'custom_config_body="{new_body}"', attrs, count=1)
                return f"<o {attrs2} />"
            # ensure QQ/Douyin-style stay rao true
            if pkg in ("com.tencent.mobileqq", "com.ss.android.ugc.aweme", "com.tencent.mm"):
                if "^rao^:^true^" not in body and '"rao":"true"' not in body:
                    stats["force_rao_known"] += 1
                    attrs2 = re.sub(r'custom_config_body="[^"]*"', f'custom_config_body="{SAFE_BODY_CARET}"', attrs, count=1)
                    return f"<o {attrs2} />"
            stats["status1_kept"] += 1
            return m.group(0)

        stats["other"] += 1
        return m.group(0)

    new_xml = pat.sub(repl, xml)

    # Ensure version bump note in comment? keep version tag but bump date for tracking
    new_xml = re.sub(r"<version>\d+</version>", "<version>20261106</version>", new_xml, count=1)

    # Add missing packages before </filter-conf>
    existing = set(re.findall(r'package_name="([^"]+)"', new_xml))
    adds = []
    for pkg in ADD_FO_PKGS:
        if pkg not in existing:
            adds.append(
                f'    <o package_name="{pkg}" status="1" use_function="fullorientation" '
                f'custom_config_body="{SAFE_BODY_CARET}" />'
            )
            stats["added"] += 1
        else:
            stats["add_already"] += 1
    if adds:
        new_xml = new_xml.replace("</filter-conf>", "\n".join(adds) + "\n</filter-conf>")

    return new_xml, stats

def transform_fantasy(xml: str):
    stats = Counter()
    existing = set(re.findall(r'package_name="([^"]+)"', xml))
    adds = []
    for pkg in ADD_MAGIC_PKGS:
        if pkg in existing:
            stats["magic_already"] += 1
            continue
        adds.append(MAGIC_TMPL.format(pkg=pkg))
        stats["magic_added"] += 1
    if adds:
        xml = xml.replace("</filter-conf>", "\n".join(adds) + "\n</filter-conf>")
        xml = re.sub(r"<version>\d+</version>", "<version>20261106</version>", xml, count=1)
    return xml, stats

def patch_db(src_db: Path, dst_db: Path, fo_enabled_pkgs: set[str], pkgs_installed: set[str]):
    shutil.copy2(src_db, dst_db)
    c = sqlite3.connect(str(dst_db))
    stats = Counter()

    # FO: for every fullorientation row, apply same policy
    rows = c.execute(
        "select package_name, status, custom_config_body, config, installed from t_config where use_function='fullorientation'"
    ).fetchall()
    for pkg, st, body, cfg, inst in rows:
        body = body or ""
        rotate_cam = "true" if '"rotate_cam":"true"' in body or "^rotate_cam^:^true^" in body else "false"
        new_body = json.dumps({"rao": "true", "rotate_cam": rotate_cam}, separators=(",", ":"))
        new_cfg = new_body
        if pkg in FO_OFF_DENY:
            if st != 0:
                c.execute(
                    "update t_config set status=0, custom_config_body=?, config=? where package_name=? and use_function='fullorientation'",
                    (SAFE_BODY_JSON, SAFE_BODY_JSON, pkg),
                )
                stats["db_deny_off"] += 1
            continue
        need = (st != 1) or ("alwaysFullOrientActivities" in body) or ("orientForStarting" in body) or ('"rao":"true"' not in body)
        # For status=1 with only camActivities (luna), still force rao true simple? Keep camActivities apps: if only camActivities and status=1, upgrade rao
        if st == 1 and '"rao":"true"' in body and "alwaysFullOrientActivities" not in body and "orientForStarting" not in body:
            stats["db_fo_ok"] += 1
            # still mark installed if needed
        elif need or st in (0, 2):
            c.execute(
                "update t_config set status=1, custom_config_body=?, config=? where package_name=? and use_function='fullorientation'",
                (new_body, new_cfg, pkg),
            )
            stats["db_fo_updated"] += 1

        if pkg in pkgs_installed:
            c.execute(
                "update t_config set installed=1 where package_name=?",
                (pkg,),
            )

    # Insert FO for ADD pkgs missing in DB
    for pkg in ADD_FO_PKGS:
        exists = c.execute(
            "select 1 from t_config where package_name=? and use_function='fullorientation'", (pkg,)
        ).fetchone()
        inst = 1 if pkg in pkgs_installed else 0
        if not exists:
            c.execute(
                "insert into t_config(package_name,use_function,config,data_sources,status,custom_mode,custom_config_body,func_version,installed) values (?,?,?,?,?,?,?,?,?)",
                (pkg, "fullorientation", SAFE_BODY_JSON, 1, 1, -1, SAFE_BODY_JSON, "1.0", inst),
            )
            stats["db_fo_inserted"] += 1
        else:
            c.execute(
                "update t_config set status=1, custom_config_body=?, config=?, installed=? where package_name=? and use_function='fullorientation'",
                (SAFE_BODY_JSON, SAFE_BODY_JSON, inst, pkg),
            )
            stats["db_fo_upserted"] += 1

    # Magic: do NOT flip Douyin/QQ magic to 1 (keep FO primary). Ensure WeChat magic stays 1.
    # Add magic rows for ADD_MAGIC_PKGS missing
    magic_body = json.dumps({
        "force_custom_pw_mode": "true",
        "mode": "1",
        "fullOrientation": "true",
        "activityPairs": [{"from": "MainActivity", "to": "*"}],
        "noRelaunchOnResize": "true",
        "adjustDisplayRotation": "0",
        "blockSensor": "true",
        "scaleWindow": "-1",
    }, separators=(",", ":"))
    for pkg in ADD_MAGIC_PKGS:
        exists = c.execute(
            "select status from t_config where package_name=? and use_function='magicwindow'", (pkg,)
        ).fetchone()
        inst = 1 if pkg in pkgs_installed else 0
        if not exists:
            c.execute(
                "insert into t_config(package_name,use_function,config,data_sources,status,custom_mode,custom_config_body,func_version,installed) values (?,?,?,?,?,?,?,?,?)",
                (pkg, "magicwindow", '{"mode":"1"}', 1, 1, -1, magic_body, "1.5", inst),
            )
            stats["db_magic_inserted"] += 1
        else:
            # only enable if currently 0; leave 2 alone (PAD exclude intentional for FO priority apps)
            st = exists[0]
            if st == 0:
                c.execute(
                    "update t_config set status=1, custom_config_body=?, installed=? where package_name=? and use_function='magicwindow'",
                    (magic_body, inst, pkg),
                )
                stats["db_magic_enabled"] += 1

    # Keep QQ/Douyin magic at 2 with excludeDevice PAD so FO wins
    for pkg in ("com.tencent.mobileqq", "com.ss.android.ugc.aweme"):
        c.execute(
            "update t_config set status=2, config=? where package_name=? and use_function='magicwindow'",
            ('{"mode":"1","excludeDevice":"PAD"}', pkg),
        )
        stats["db_magic_keep_off_for_fo"] += 1

    # WeChat FO must be 1 simple
    c.execute(
        "update t_config set status=1, custom_config_body=?, config=? where package_name='com.tencent.mm' and use_function='fullorientation'",
        (SAFE_BODY_JSON, SAFE_BODY_JSON),
    )
    stats["db_wechat_fo"] += 1

    c.commit()

    # summary counts
    fo_counts = c.execute(
        "select status, count(*) from t_config where use_function='fullorientation' group by status"
    ).fetchall()
    magic_counts = c.execute(
        "select status, count(*) from t_config where use_function='magicwindow' group by status"
    ).fetchall()
    installed_fo = c.execute(
        "select package_name, status, custom_config_body from t_config where use_function='fullorientation' and installed=1"
    ).fetchall()
    c.close()
    return stats, fo_counts, magic_counts, installed_fo

def main():
    pkgs3 = set(load_pkgs3())
    # also treat known present systemish apps as installed
    pkgs_installed = set(pkgs3) | set(ADD_FO_PKGS)

    fo_src = LIVE_FO.read_text(encoding="utf-8")
    fo_new, fo_stats = transform_fo(fo_src)
    fo_path = OUT / "sys_full_orientation_managed.bulk-v1.xml"
    fo_path.write_text(fo_new, encoding="utf-8", newline="\n")
    # also save pre image
    shutil.copy2(LIVE_FO, OUT / "sys_full_orientation_managed.pre-bulk.xml")

    fw_src = LIVE_FW.read_text(encoding="utf-8")
    fw_new, fw_stats = transform_fantasy(fw_src)
    fw_path = OUT / "sys_fantasy_window_managed.bulk-v1.xml"
    fw_path.write_text(fw_new, encoding="utf-8", newline="\n")
    shutil.copy2(LIVE_FW, OUT / "sys_fantasy_window_managed.pre-bulk.xml")

    db_out = OUT / "fantasywindow.bulk-v1.db"
    db_stats, fo_counts, magic_counts, installed_fo = patch_db(LIVE_DB, db_out, set(), pkgs_installed)

    report = {
        "fo_xml_md5_pre": md5_text(fo_src),
        "fo_xml_md5_post": md5_text(fo_new),
        "fo_xml_bytes_post": len(fo_new.encode()),
        "fo_transform_stats": dict(fo_stats),
        "fantasy_xml_md5_pre": md5_text(fw_src),
        "fantasy_xml_md5_post": md5_text(fw_new),
        "fantasy_transform_stats": dict(fw_stats),
        "db_stats": dict(db_stats),
        "db_fo_status_counts": fo_counts,
        "db_magic_status_counts": magic_counts,
        "db_installed_fo": [(p, s, (b or "")[:80]) for p, s, b in installed_fo],
        "pkgs3_count": len(pkgs3),
    }
    (OUT / "bake-report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    # human summary
    lines = []
    lines.append(f"FO XML {report['fo_xml_md5_pre']} -> {report['fo_xml_md5_post']}")
    lines.append(f"FO transform: {dict(fo_stats)}")
    lines.append(f"Fantasy transform: {dict(fw_stats)}")
    lines.append(f"DB stats: {dict(db_stats)}")
    lines.append(f"DB FO status counts: {fo_counts}")
    lines.append(f"DB magic status counts: {magic_counts}")
    lines.append("Installed FO after:")
    for row in installed_fo:
        lines.append(f"  {row}")
    # FO status counts in new XML
    stc = Counter(re.findall(r'<o package_name="[^"]+" status="(\d)"', fo_new))
    lines.append(f"FO XML status counts: {dict(stc)}")
    (OUT / "bake-report.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print("WROTE", fo_path)
    print("WROTE", fw_path)
    print("WROTE", db_out)

if __name__ == "__main__":
    main()
