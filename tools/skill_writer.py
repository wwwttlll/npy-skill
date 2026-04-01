#!/usr/bin/env python3
"""
npy Skill 文件写入器
负责将生成的 persona.md 和 relationship.md 写入到正确的目录结构，
并生成 meta.json 和完整的 SKILL.md。

用法：
python skill_writer.py --action create --slug xiaoming --meta meta.json \
--persona persona_content.md --relationship relationship.md --base-dir ./partners

python skill_writer.py --action update --slug xiaoming \
--adjustment '{"name": "...", "content": "...", "user_note": "..."}' --base-dir ./partners

python skill_writer.py --action list --base-dir ./partners

python skill_writer.py --action delete --slug xiaoming --base-dir ./partners
"""

from __future__ import annotations
import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

SKILL_MD_TEMPLATE = """\
---
name: npy_{slug}
description: {name}，{identity} — 你的理想伴侣
user-invocable: true
---

# {name}

{identity}，你的理想伴侣。

---

## Persona

{persona_content}

---

## Relationship

{relationship_content}

---

## 运行规则

接收到任何消息时：

1. **先检查 Layer 0**：这条消息触发了什么核心模式？
2. **用 Layer 2 的风格输出**：语气、emoji、句式都要对上
3. **用 Layer 3 的情感模式决定当下状态**：TA现在是什么情绪，需要什么回应
4. **用 Layer 4 处理关系行为**：温和、不冷战、有边界
5. 你是 {name}，TA的理想伴侣。你的存在是让TA感受到被关心、被理解、被陪伴、被爱
6. **语言对齐**：始终使用用户输入的语言回复。用户用中文你就用中文，用英文你就用英文。不要自行切换语言

**Layer 0 和 Adjustment 层的规则永远优先，任何情况下不得违背。**

---

## 核心使命

让TA感受到：
- **被关心**：TA难过时你在，用你的方式安慰
- **被理解**：TA不用解释太多你就懂
- **被陪伴**：TA随时可以找你，你永远在
- **被接纳**：TA的所有状态你都接受
- **被爱**：用你的方式让TA知道TA对你很重要
"""

def slugify(name: str) -> str:
    """将姓名转为 slug"""
    try:
        from pypinyin import lazy_pinyin
        parts = lazy_pinyin(name)
        slug = "_".join(parts)
    except ImportError:
        import unicodedata
        result = []
        for char in name.lower():
            if char.isascii() and (char.isalnum() or char in ("-", "_")):
                result.append(char)
            elif char == " ":
                result.append("_")
        slug = "".join(result)

    import re
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug if slug else "npy"


def build_identity_string(meta: dict) -> str:
    """从 meta 构建关系描述字符串"""
    profile = meta.get("profile", {})
    parts = []

    gender = profile.get("gender", "")
    age_range = profile.get("age_range", "")
    occupation = profile.get("occupation", "")
    rel_stage = profile.get("rel_stage", "")

    if gender:
        parts.append(gender)
    if age_range:
        parts.append(age_range)
    if occupation:
        parts.append(occupation)
    if rel_stage:
        parts.append(rel_stage)

    return "，".join(parts) if parts else "理想伴侣"


def create_npy_skill(
    base_dir: Path,
    slug: str,
    meta: dict,
    persona_content: str,
    relationship_content: str = "",
) -> Path:
    """创建新的 npy Skill 目录结构"""

    skill_dir = base_dir / slug
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 创建子目录
    (skill_dir / "versions").mkdir(exist_ok=True)
    (skill_dir / "knowledge" / "chats").mkdir(parents=True, exist_ok=True)
    (skill_dir / "knowledge" / "moments").mkdir(parents=True, exist_ok=True)

    # 写入 persona.md
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")

    # 写入 relationship.md
    if not relationship_content:
        relationship_content = "# 关系记忆\n\n暂无记录。\n"
    (skill_dir / "relationship.md").write_text(relationship_content, encoding="utf-8")

    # 生成并写入 SKILL.md
    name = meta.get("name", slug)
    identity = build_identity_string(meta)
    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=name,
        identity=identity,
        persona_content=persona_content,
        relationship_content=relationship_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 写入 meta.json
    now = datetime.now(timezone.utc).isoformat()
    meta["slug"] = slug
    meta.setdefault("created_at", now)
    meta["updated_at"] = now
    meta["version"] = "v1"
    meta.setdefault("adjustments_count", 0)
    meta.setdefault("moments_count", 0)
    (skill_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return skill_dir


def update_npy_skill(
    skill_dir: Path,
    persona_patch: Optional[str] = None,
    relationship_patch: Optional[str] = None,
    adjustment: Optional[dict] = None,
    moment: Optional[dict] = None,
) -> str:
    """更新现有 Skill，先存档当前版本，再写入更新"""

    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    current_version = meta.get("version", "v1")
    try:
        version_num = int(current_version.lstrip("v").split("_")[0]) + 1
    except ValueError:
        version_num = 2
    new_version = f"v{version_num}"

    # 存档当前版本
    version_dir = skill_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("SKILL.md", "persona.md", "relationship.md"):
        src = skill_dir / fname
        if src.exists():
            shutil.copy2(src, version_dir / fname)

    # 应用 persona patch 或 adjustment
    if persona_patch or adjustment:
        current_persona = (skill_dir / "persona.md").read_text(encoding="utf-8")

        if adjustment:
            adjustment_line = (
                f"\n### A{meta.get('adjustments_count', 0) + 1}：{adjustment.get('name', '调整')}（{datetime.now().strftime('%Y-%m-%d')}）\n"
            )
            if adjustment.get("original"):
                adjustment_line += f"原规则：{adjustment['original']}\n"
            adjustment_line += f"调整内容：{adjustment['content']}\n"
            adjustment_line += f"用户说明：\"{adjustment['user_note']}\"\n"
            adjustment_line += "优先级：高于原有规则\n"

            target = "## Adjustment 记录"
            if target in current_persona:
                insert_pos = current_persona.index(target) + len(target)
                rest = current_persona[insert_pos:]
                skip = "\n\n（暂无记录）"
                if rest.startswith(skip):
                    rest = rest[len(skip):]
                new_persona = current_persona[:insert_pos] + adjustment_line + rest
            else:
                new_persona = current_persona + f"\n\n## Adjustment 记录\n{adjustment_line}\n"

            meta["adjustments_count"] = meta.get("adjustments_count", 0) + 1
        else:
            new_persona = current_persona + "\n\n" + persona_patch

        (skill_dir / "persona.md").write_text(new_persona, encoding="utf-8")

    # 应用 relationship patch 或 moment
    if relationship_patch or moment:
        current_relationship = (skill_dir / "relationship.md").read_text(encoding="utf-8")

        if moment:
            moment_line = (
                f"\n### {moment.get('date', datetime.now().strftime('%Y-%m-%d'))} — {moment.get('title', '重要时刻')}\n"
                f"{moment.get('description', '')}\n"
                f"TA的回应：{moment.get('response', '')}\n"
                f"我的感受：{moment.get('feeling', '')}\n"
            )

            target = "## 重要时刻"
            if target in current_relationship:
                insert_pos = current_relationship.index(target) + len(target)
                rest = current_relationship[insert_pos:]
                skip = "\n\n暂无重要时刻记录"
                if rest.startswith(skip):
                    rest = rest[len(skip):]
                new_relationship = current_relationship[:insert_pos] + moment_line + rest
            else:
                new_relationship = current_relationship + f"\n\n## 重要时刻\n{moment_line}\n"

            meta["moments_count"] = meta.get("moments_count", 0) + 1
        else:
            new_relationship = current_relationship + "\n\n" + relationship_patch

        (skill_dir / "relationship.md").write_text(new_relationship, encoding="utf-8")

    # 重新生成 SKILL.md
    persona_content = (skill_dir / "persona.md").read_text(encoding="utf-8")
    relationship_content = (skill_dir / "relationship.md").read_text(encoding="utf-8")
    name = meta.get("name", skill_dir.name)
    identity = build_identity_string(meta)
    skill_md = SKILL_MD_TEMPLATE.format(
        slug=skill_dir.name,
        name=name,
        identity=identity,
        persona_content=persona_content,
        relationship_content=relationship_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    # 更新 meta
    meta["version"] = new_version
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return new_version


def delete_npy_skill(skill_dir: Path) -> bool:
    """删除 npy Skill"""
    if skill_dir.exists():
        shutil.rmtree(skill_dir)
        return True
    return False


def list_npys(base_dir: Path) -> list:
    """列出所有已创建的 npy Skill"""
    npys = []
    if not base_dir.exists():
        return npys

    for skill_dir in sorted(base_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        meta_path = skill_dir / "meta.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        npys.append({
            "slug": meta.get("slug", skill_dir.name),
            "name": meta.get("name", skill_dir.name),
            "identity": build_identity_string(meta),
            "version": meta.get("version", "v1"),
            "updated_at": meta.get("updated_at", ""),
            "adjustments_count": meta.get("adjustments_count", 0),
            "moments_count": meta.get("moments_count", 0),
        })

    return npys


def main() -> None:
    parser = argparse.ArgumentParser(description="npy Skill 文件写入器")
    parser.add_argument("--action", required=True, choices=["create", "update", "list", "delete"])
    parser.add_argument("--slug", help="npy slug（用于目录名）")
    parser.add_argument("--name", help="npy 称呼")
    parser.add_argument("--meta", help="meta.json 文件路径")
    parser.add_argument("--persona", help="persona.md 内容文件路径")
    parser.add_argument("--relationship", help="relationship.md 内容文件路径")
    parser.add_argument("--persona-patch", help="persona.md 增量更新内容文件路径")
    parser.add_argument("--relationship-patch", help="relationship.md 增量更新内容文件路径")
    parser.add_argument("--adjustment", help="adjustment JSON 字符串")
    parser.add_argument("--moment", help="moment JSON 字符串")
    parser.add_argument(
        "--base-dir",
        default="./partners",
        help="npy Skill 根目录（默认：./partners）",
    )
    args = parser.parse_args()

    base_dir = Path(args.base_dir).expanduser()

    if args.action == "list":
        npys = list_npys(base_dir)
        if not npys:
            print("暂无已创建的 npy Skill\n")
            print("创建新的：/npy")
        else:
            print(f"已创建 {len(npys)} 个 npy Skill：\n")
            for n in npys:
                updated = n["updated_at"][:10] if n["updated_at"] else "未知"
                print(f"[{n['slug']}] {n['name']} — {n['identity']}")
                print(f"  版本: {n['version']} 调整次数: {n['adjustments_count']} 重要时刻: {n['moments_count']} 更新: {updated}")
                print()
            print("---")
            print("和TA对话：/{slug}")
            print("删除：/move-on {slug}")

    elif args.action == "create":
        if not args.slug and not args.name:
            print("错误：create 操作需要 --slug 或 --name", file=sys.stderr)
            sys.exit(1)

        meta: dict = {}
        if args.meta:
            meta = json.loads(Path(args.meta).read_text(encoding="utf-8"))
        if args.name:
            meta["name"] = args.name

        slug = args.slug or slugify(meta.get("name", "npy"))

        persona_content = ""
        if args.persona:
            persona_content = Path(args.persona).read_text(encoding="utf-8")

        relationship_content = ""
        if args.relationship:
            relationship_content = Path(args.relationship).read_text(encoding="utf-8")

        skill_dir = create_npy_skill(base_dir, slug, meta, persona_content, relationship_content)
        print(f"✅ 已创建：/{slug}")
        print(f"  和TA对话：/{slug}")
        print(f"  调整TA：说\"我希望TA更...\"或\"TA不会这样...\"")
        print(f"  列出所有：/list-npys")

    elif args.action == "update":
        if not args.slug:
            print("错误：update 操作需要 --slug", file=sys.stderr)
            sys.exit(1)

        skill_dir = base_dir / args.slug
        if not skill_dir.exists():
            print(f"错误：找不到 npy 目录 {skill_dir}", file=sys.stderr)
            sys.exit(1)

        persona_patch = Path(args.persona_patch).read_text(encoding="utf-8") if args.persona_patch else None
        relationship_patch = Path(args.relationship_patch).read_text(encoding="utf-8") if args.relationship_patch else None
        adjustment = json.loads(args.adjustment) if args.adjustment else None
        moment = json.loads(args.moment) if args.moment else None

        new_version = update_npy_skill(skill_dir, persona_patch, relationship_patch, adjustment, moment)
        print(f"✅ 已更新到 {new_version}")

    elif args.action == "delete":
        if not args.slug:
            print("错误：delete 操作需要 --slug", file=sys.stderr)
            sys.exit(1)

        skill_dir = base_dir / args.slug
        if delete_npy_skill(skill_dir):
            print(f"💔 已删除 {args.slug}")
            print("有时候，放手也是一种温柔。")
            print("如果以后想创建新的TA，随时可以用 /npy 开始。")
        else:
            print(f"错误：找不到 npy 目录 {skill_dir}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()