/* SPDX-License-Identifier: GPL-2.0-only */
#ifndef __EROFS_COMPAT_H
#define __EROFS_COMPAT_H
/* Private 4.19 equivalents of the newer pagemap helpers. */
#include <linux/pagemap.h>
#include <linux/magic.h>
#ifndef EROFS_SUPER_MAGIC_V1
#define EROFS_SUPER_MAGIC_V1 0xE0F5E1E2
#endif
static inline void erofs_attach_page_private(struct page *page, void *data)
{
 get_page(page);
 set_page_private(page, (unsigned long)data);
 SetPagePrivate(page);
}
static inline void *erofs_detach_page_private(struct page *page)
{
 void *data = (void *)page_private(page);
 if (!PagePrivate(page)) return NULL;
 ClearPagePrivate(page);
 set_page_private(page, 0);
 put_page(page);
 return data;
}

#endif /* __EROFS_COMPAT_H */
