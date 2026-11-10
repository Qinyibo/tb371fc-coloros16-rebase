#!/usr/bin/env python3
"""Apply Force REK diagnostic to nvt_panel_resume_commit in r108-src."""
from pathlib import Path

path = Path("/work/r108-src/drivers/input/touchscreen/nt36532/nt36xxx.c")
text = path.read_text(encoding="utf-8", errors="strict")

marker = "static int nvt_panel_resume_commit(struct device *dev, uint32_t id)"
if "R10x_FORCE_REK_SENT" in text:
    print("Force REK already present")
    raise SystemExit(0)

helper = r'''
/* Diagnostic: host Force-Cal / ReK (0x23 0x00) before native REK wait.
 * Uses this tree's nvt_set_page + CTP_SPI_WRITE HOST_CMD path only.
 * IRQ stays closed; success still requires real RESET_STATE_REK. */
static int nvt_force_rek_host_cmd(void)
{
	uint8_t cmd[3] = { EVENT_MAP_HOST_CMD, 0x23, 0x00 };
	uint8_t st[6] = {0};
	int ret;

	ret = nvt_set_page(ts->mmap->EVENT_BUF_ADDR | EVENT_MAP_RESET_COMPLETE);
	if (!ret) {
		st[0] = EVENT_MAP_RESET_COMPLETE;
		if (!CTP_SPI_READ(ts->client, st, 6))
			NVT_LOG("R10x_FORCE_REK_PRE_STATE=0x%02X\n", st[1]);
	}

	ret = nvt_set_page(ts->mmap->EVENT_BUF_ADDR | EVENT_MAP_HOST_CMD);
	if (ret) {
		NVT_ERR("R10x_FORCE_REK_PAGE_FAILED %d\n", ret);
		return ret;
	}
	ret = CTP_SPI_WRITE(ts->client, cmd, sizeof(cmd));
	if (ret) {
		NVT_ERR("R10x_FORCE_REK_WRITE_FAILED %d\n", ret);
		return ret;
	}
	NVT_LOG("R10x_FORCE_REK_SENT cmd=0x23 0x00\n");
	usleep_range(10000, 10000);
	return 0;
}

'''

if marker not in text:
    raise SystemExit("commit marker not found")

text = text.replace(marker, helper + marker, 1)

old = """    if (!nvt_panel_resume_armed) {
        ret = -EAGAIN;
        goto out;
    }
    ret = nvt_check_fw_reset_state(RESET_STATE_REK);
    if (ret) {
        r94_wake_error(R94_WAKE_COMMIT, ret);
        NVT_ERR("R94_NATIVE_COMPLETE_REK_FAILED %d IRQ_CLOSED_DISPLAY_RETAINED\\n", ret);
        goto out;
    }
"""

new = """    if (!nvt_panel_resume_armed) {
        ret = -EAGAIN;
        goto out;
    }
    /* One diagnostic Force-REK before the real REK gate. Do not fake A3,
     * do not open IRQ on failure, and do not skip the REK wait. */
    (void)nvt_force_rek_host_cmd();
    ret = nvt_check_fw_reset_state(RESET_STATE_REK);
    if (ret) {
        uint8_t st[6] = {0};
        if (!nvt_set_page(ts->mmap->EVENT_BUF_ADDR | EVENT_MAP_RESET_COMPLETE)) {
            st[0] = EVENT_MAP_RESET_COMPLETE;
            if (!CTP_SPI_READ(ts->client, st, 6))
                NVT_ERR("R10x_FORCE_REK_STATE=0x%02X FAIL\\n", st[1]);
        }
        r94_wake_error(R94_WAKE_COMMIT, ret);
        NVT_ERR("R94_NATIVE_COMPLETE_REK_FAILED %d IRQ_CLOSED_DISPLAY_RETAINED\\n", ret);
        goto out;
    }
    NVT_LOG("R10x_FORCE_REK_STATE_OK >=REK\\n");
"""

if old not in text:
    raise SystemExit("commit REK block not found for replacement")

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("patched", path)
print("markers:", text.count("R10x_FORCE_REK_SENT"), text.count("R10x_FORCE_REK_STATE_OK"))
