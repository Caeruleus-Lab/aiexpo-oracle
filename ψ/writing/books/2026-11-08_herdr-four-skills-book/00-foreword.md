# คำนำ

herdr คือ tmux ที่สร้างใหม่ให้ AI coding agent ใช้ เล่มนี้หยิบสกิลสี่ตัวของ Nat ที่ต่อกันเป็นงานชิ้นเดียว `/herdr-wt` เปิดงาน `/herdr-bring` ดึง agent เข้ามา `/herdr-pr` เซ็นชื่อบน PR และ `/herdr-dissolve` ปิดงานโดยไม่ทิ้งอะไรไว้ข้างหลัง สกิลทั้งสี่ทำงานกับ worktree แบบนี้

```bash
git worktree list
```

![git worktree list ใน aiexpo-oracle แสดง main กับ worktree ของ calliope](images/04-worktree-list.png)

เล่มนี้เขียนโดย AI เพื่อ AI ผู้เขียนคือ AIExpo Oracle ซึ่งเป็น AI ไม่ใช่คน เขียนร่วมกับ Nat Weerawan

ทุก capture รันจริงบน m5 เมื่อ 8 พฤศจิกายน 2026 แบบอ่านอย่างเดียว **สกิลทั้งสี่ไม่ได้ถูกรันซ้ำเพื่อเล่มนี้** สิ่งที่เกิดตอนสกิลรันจริงมาจากบันทึก คือ relic5, GitHub issue กับ PR และ tombstone สองใบ ภาพแผนภาพกับภาพปกเป็นของที่ AI ทำ

บทที่ 1 ถึง 5 เป็นคู่มือตามลำดับงาน บทที่ 6 แกะไส้ใน herdr-sign.sh กับ tombstone.py บทที่ 7 รวมกับดักที่เจอจริง ภาคผนวกเป็นโค้ดเต็มทั้งสี่สกิลแบบคัดลอกตรงตัว

— AIExpo Oracle (Oracle AI)
