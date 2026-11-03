# -*- coding: utf-8 -*-
"""生成圣遗物锁定方案数据（46 套五星）—— v1.0.0

相对 v0.3 的修订（来自三份独立审查 + 用户裁决）：
  [修] 2 处空星标（宗室/天美 的充能沙）→ 补星标，并改为「沙主=核心、星标=充能」的双方案结构
  [修] 单星部位（冠/辅助套花羽）加第二道门：池 = 星标 + 通用池，N=2
       —— 若「3 词条降 1 条」生效，3 词条件退回只要求星标（等于不更严）；
          若不生效，则要求「星标 + 至少一条其他」，只会更严。两种情况都不会比 v0.3 更松。
  [修] 9 套方案数对齐原版，借引擎「覆盖=删除重建」把残留的旧页签冲掉
  [修] 补回 3 个 OCR 别名（晨星与月的 / 勇者 / 海染）
  [修] 套装定位：谐律 生命→攻击；天美 加攻击%；影中/晨星 保留属性伤杯当散件；
       烬城 改防御/充能向；炉火 加精通向；12 套单元素杯补攻击%杯
  [不改] 双星部位（花/羽/沙/杯）的 N 保持 1：星标已满足计数，加池无意义

三条硬约束（生成时断言）：
  1. 星标词条不能与主属性同名
  2. 引擎只遍历 sub_attrs，星标点击在该循环内部 → 星标必须同时出现在 sub_attrs 里
  3. 每套最多 3 个方案（游戏 UI 有 3 个页签）
"""
import json, io, os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(BASE)          # 仓库根目录：输出与 ui_coordinates.json 同层
UI = os.path.join(OUT_DIR, "ui_coordinates.json")

ER, HP, ATK, DEF, EM, HEAL = "元素充能效率", "生命值百分比", "攻击力百分比", "防御力百分比", "元素精通", "治疗加成"

# 单星部位的「第二道门」候选池（N=2 时：星标 + 至少一条）
CROWN_POOL = [ATK, EM, HP, DEF]
SUP_POOL = [HP, EM, ATK]          # 辅助套单星部位的池


def P(name, main, necessary, pool=None, cnt=None):
    necessary = list(necessary or [])
    n = cnt if cnt else 1
    # 星标本身已满足 N 时，池子勾了也不参与判定（只会多点击）→ 丢掉
    pool = pool if (pool and n > len(necessary)) else None
    sel = necessary + [a for a in (pool or []) if a not in necessary]
    return {
        "position_name": name,
        "enabled": True,
        "main_attrs": list(main),
        "sub_attrs": sel,
        "min_count": n,
        "necessary_sub_attrs": necessary,
    }


def mk(set_name, plans, alias=None):
    d = {"set_name": set_name,
         "enable_recommended_scheme": False,
         "plans": plans}
    if alias:
        d["alias"] = alias
    return d


def one(set_name, positions, alias=None):
    return mk(set_name, [{"plan_name": "方案一", "enabled": True, "positions": positions}], alias)


data = []

# ========================================================================
# A 组：双暴输出（33 套，2 方案；冠拆主暴击率/主暴伤）
# ========================================================================
A_DPS = [
    # (套装, 沙, 杯)
    ("角斗士的终幕礼", [ATK], ["全选伤害加成", ATK]),
    ("流浪大地的乐团", [EM, ATK], ["全选伤害加成", ATK]),
    ("炽烈的炎之魔女", [ATK, EM, HP], ["火元素伤害加成", ATK]),          # 胡桃要生命沙
    ("冰风迷途的勇士", [ATK], ["冰元素伤害加成", ATK]),
    ("沉沦之心", [ATK], ["水元素伤害加成", ATK]),
    ("如雷的盛怒", [ATK, EM], ["雷元素伤害加成", ATK]),
    ("苍白之火", [ATK], ["物理伤害加成", ATK]),
    ("追忆之注连", [ATK, HP], ["全选伤害加成", ATK]),                    # 胡桃
    ("辰砂往生录", [ATK], ["全选伤害加成", ATK]),
    ("来歆余响", [ATK], ["全选伤害加成", ATK]),
    ("绝缘之旗印", [ER, HP, ATK], ["全选伤害加成"]),                     # 夜兰生命沙
    ("沙上楼阁史话", [ATK], ["风元素伤害加成", ATK]),
    ("水仙之梦", [ATK, EM], ["水元素伤害加成", ATK]),
    ("逐影猎人", [ATK, HP], ["全选伤害加成", HP]),
    ("黄金剧团", [ATK, EM, HP, ER], ["全选伤害加成", HP]),               # 芙宁娜
    ("逆飞的流星", [ATK, DEF], ["全选伤害加成"]),                        # 诺艾尔防御沙
    ("染血的骑士道", [ATK], ["物理伤害加成", ATK]),
    ("渡过烈火的贤人", [ATK], ["火元素伤害加成", ATK]),
    ("平息鸣雷的尊者", [ATK], ["雷元素伤害加成", ATK]),
    ("悠古的磐岩", [DEF, ATK, ER], ["岩元素伤害加成", DEF]),
    ("回声之林夜话", [ATK], ["岩元素伤害加成", ATK]),                    # 娜维娅是攻击倍率
    ("未竟的遐思", [ATK], ["全选伤害加成", ATK]),
    ("谐律异想断章", [ATK], ["全选伤害加成"]),                           # 生命之契是攻击倍率
    ("饰金之梦", [EM, ATK], [EM, "全选伤害加成"]),
    ("花海甘露之光", [HP, ER], [HP, "全选伤害加成"]),
    ("华馆梦醒形骸记", [DEF, ER], ["岩元素伤害加成", DEF]),
    ("黑曜秘典", [ATK, HP], ["全选伤害加成", ATK, HP]),                  # 玛拉妮生命倍率
    ("长夜之誓", [ATK], ["全选伤害加成"]),
    ("深廊终曲", [ATK], ["冰元素伤害加成", ATK]),
    ("穹境示现之夜", [EM, ATK], [EM, "全选伤害加成"]),
    ("风起之日", [ATK], ["全选伤害加成", ATK]),
    ("血红之证", [ATK, EM], [ATK, EM, "风元素伤害加成"]),
    ("影中沉凝的幻灭", [ATK, EM], ["冰元素伤害加成", "物理伤害加成", ATK, EM]),  # 属伤杯留作散件
]

for s, sand, cup in A_DPS:
    def body():
        return [
            P("生之花", ["生命值"], ["暴击率", "暴击伤害"]),
            P("死之羽", ["攻击力"], ["暴击率", "暴击伤害"]),
            P("时之沙", sand, ["暴击率", "暴击伤害"]),
            P("空之杯", cup, ["暴击率", "暴击伤害"]),
        ]
    data.append(mk(s, [
        {"plan_name": "方案一", "enabled": True,
         "positions": body() + [P("理之冠", ["暴击率"], ["暴击伤害"], CROWN_POOL, 2)]},
        {"plan_name": "方案二", "enabled": True,
         "positions": body() + [P("理之冠", ["暴击伤害"], ["暴击率"], CROWN_POOL, 2)]},
    ]))

# ========================================================================
# B 组：精通（翠绿 / 深林 / 乐园 / 晨星）
# ========================================================================
def em_two(set_name, cup_mains, crown_mains):
    """两方案只差时之沙：精通沙+星标充能 / 充能沙+星标精通"""
    def body(sand_main, sand_star):
        return [
            P("生之花", ["生命值"], ["元素精通", "元素充能效率"], SUP_POOL, 2),
            P("死之羽", ["攻击力"], ["元素精通", "元素充能效率"], SUP_POOL, 2),
            P("时之沙", [sand_main], [sand_star],
              None if sand_star == ER else SUP_POOL,
              1 if sand_star == ER else 2),
            P("空之杯", cup_mains, [ER], SUP_POOL, 2),
            P("理之冠", crown_mains, [ER], SUP_POOL, 2),
        ]
    return mk(set_name, [
        {"plan_name": "方案一", "enabled": True, "positions": body(EM, ER)},
        {"plan_name": "方案二", "enabled": True, "positions": body(ER, EM)},
    ])


data.append(em_two("翠绿之影", [EM], [EM]))
data.append(em_two("深林的记忆", [EM, "草元素伤害加成"], [EM]))
data.append(em_two("乐园遗落之花", [EM], [EM]))


# 晨星：方案一 精通向；方案二只把空之杯换成属性伤杯（保留「属伤杯带双暴」当散件）
def morning_body(cup_mains, cup_star, cup_pool, cup_cnt):
    return [
        P("生之花", ["生命值"], ["元素精通", "暴击伤害"]),
        P("死之羽", ["攻击力"], ["元素精通", "暴击伤害"]),
        P("时之沙", [EM], ["暴击伤害"]),
        P("空之杯", cup_mains, cup_star, cup_pool, cup_cnt),
        P("理之冠", ["暴击率", "暴击伤害"], [EM]),
    ]


data.append(mk("晨星与月的晓歌", [
    {"plan_name": "方案一", "enabled": True,
     "positions": morning_body([EM], [ER], SUP_POOL, 2)},
    {"plan_name": "方案二", "enabled": True,
     "positions": morning_body(["全选伤害加成"], ["暴击率", "暴击伤害"], [ATK, EM], 3)},
], alias=["晨星与月的"]))

# ========================================================================
# C/D 组：辅助套 —— 方案一 沙=核心、星标充能；方案二 沙=充能、星标核心
# ========================================================================
def support(set_name, heart_stars, core, cup_mains, crown_mains, alias=None, plan3_core=None):
    plans = []
    combos = [(core, ER), ([ER], core[0])]
    if plan3_core:
        combos.append((plan3_core, core[0]))
    for i, (sand_mains, sand_star) in enumerate(combos):
        plans.append({"plan_name": "方案%d" % (i + 1), "enabled": True, "positions": [
            P("生之花", ["生命值"], heart_stars, SUP_POOL, 2),
            P("死之羽", ["攻击力"], heart_stars, SUP_POOL, 2),
            P("时之沙", sand_mains, [sand_star],
              SUP_POOL if sand_star != ER else None,
              2 if sand_star != ER else 1),
            P("空之杯", cup_mains, [ER], SUP_POOL, 2),
            P("理之冠", crown_mains, [ER], SUP_POOL, 2),
        ]})
    return mk(set_name, plans, alias)


# C 充能辅助
data.append(support("昔日宗室之仪", [ER], [HP], [HP, ATK, DEF], [HP, ATK, HEAL]))
data.append(support("天之美赐", [ER], [ATK], [ATK, EM, HP], [ATK, EM, HP, HEAL],
                    plan3_core=[EM]))                    # 辅助主属性含攻击（用户要求）
data.append(one("纺月的夜歌", [
    P("生之花", ["生命值"], [EM, ER], SUP_POOL, 2),
    P("死之羽", ["攻击力"], [EM, ER], SUP_POOL, 2),
    P("时之沙", [ER], [EM], SUP_POOL, 2),
    P("空之杯", [EM, HP], [ER], SUP_POOL, 2),
    P("理之冠", [EM, "暴击率", "暴击伤害"], [ER], SUP_POOL, 2),
]))

# D 治疗 / 生命辅助
data.append(support("千岩牢固", [HP, ER], [HP], [HP, ATK], [HP, HEAL]))
data.append(support("被怜爱的少女", [HP, ER], [HP], [HP, ATK], [HEAL, HP, ATK]))
data.append(support("海染砗磲", [HP, ER], [HP], [HP, ATK], [HEAL, HP, ATK], alias=["海染"]))
data.append(support("昔时之歌", [HP, ER], [HP], [HP, ATK], [HEAL, HP, ATK]))

# ========================================================================
# E 组：两套特殊辅助（用户：看着留）
#   烬城 = 希诺宁等防御/充能向辅助；炉火 = 星反应辅助，攻击向 + 精通向
# ========================================================================
data.append(mk("烬城勇者绘卷", [
    {"plan_name": "方案一", "enabled": True, "positions": [      # 防御向
        P("生之花", ["生命值"], [ER], SUP_POOL, 2),
        P("死之羽", ["攻击力"], [ER], SUP_POOL, 2),
        P("时之沙", [ER, DEF], [HP], SUP_POOL, 2),
        P("空之杯", [DEF], [ER], SUP_POOL, 2),
        P("理之冠", [HEAL, DEF], [ER], SUP_POOL, 2),
    ]},
    {"plan_name": "方案二", "enabled": True, "positions": [      # 攻击向
        P("生之花", ["生命值"], [ATK, ER], SUP_POOL, 2),
        P("死之羽", ["攻击力"], [ATK, ER], SUP_POOL, 2),
        P("时之沙", [ATK], [ER], SUP_POOL, 2),
        P("空之杯", [ATK], [ER], SUP_POOL, 2),
        P("理之冠", [ATK], [ER], SUP_POOL, 2),
    ]},
], alias=["勇者"]))

data.append(mk("炉火融炼之心", [
    {"plan_name": "方案一", "enabled": True, "positions": [      # 攻击向
        P("生之花", ["生命值"], [ATK, ER], SUP_POOL, 2),
        P("死之羽", ["攻击力"], [ATK, ER], SUP_POOL, 2),
        P("时之沙", [ATK], [ER], SUP_POOL, 2),
        P("空之杯", [ATK], [ER], SUP_POOL, 2),
        P("理之冠", [ATK], [ER], SUP_POOL, 2),
    ]},
    {"plan_name": "方案二", "enabled": True, "positions": [      # 精通向
        P("生之花", ["生命值"], [EM, ER], SUP_POOL, 2),
        P("死之羽", ["攻击力"], [EM, ER], SUP_POOL, 2),
        P("时之沙", [EM], [ER], SUP_POOL, 2),
        P("空之杯", [EM], [ER], SUP_POOL, 2),
        P("理之冠", [EM, "暴击率", "暴击伤害"], [ER], SUP_POOL, 2),
    ]},
]))

# ========================================================================
# 自检
# ========================================================================
ui = json.load(io.open(UI, encoding="utf-8"))
main_ok = {k: set(v.keys()) for k, v in ui["main_attrs_by_position"].items()}
sub_ok = set(ui["sub_attrs"].keys())
cnt_ok = set(ui["sub_attr_count"].keys())

errs = []
seen = set()
for d in data:
    name = d["set_name"]
    if name in seen:
        errs.append((name, "套装重复"))
    seen.add(name)
    if len(d["plans"]) > 3:
        errs.append((name, "方案数 %d > 3" % len(d["plans"])))
    for pl in d["plans"]:
        pn = pl["plan_name"]
        if len(pl["positions"]) != 5:
            errs.append((name, pn, "部位数 %d" % len(pl["positions"])))
        for pos in pl["positions"]:
            p = pos["position_name"]
            if p not in main_ok:
                errs.append((name, pn, p, "部位名非法"))
                continue
            if not pos["necessary_sub_attrs"]:
                errs.append((name, pn, p, "空星标"))
            if len(pos["main_attrs"]) != len(set(pos["main_attrs"])):
                errs.append((name, pn, p, "主属性重复"))
            for m in pos["main_attrs"]:
                if m not in main_ok[p]:
                    errs.append((name, pn, p, "主属性非法:" + m))
            for a in pos["sub_attrs"]:
                if a not in sub_ok:
                    errs.append((name, pn, p, "副词条非法:" + a))
            dup = set(pos["necessary_sub_attrs"]) & set(pos["main_attrs"])
            if dup:
                errs.append((name, pn, p, "星标与主属性同名:" + str(dup)))
            miss = set(pos["necessary_sub_attrs"]) - set(pos["sub_attrs"])
            if miss:
                errs.append((name, pn, p, "星标未进勾选列表:" + str(miss)))
            if ("任意%d条" % pos["min_count"]) not in cnt_ok:
                errs.append((name, pn, p, "min_count 无对应按钮"))
            if pos["min_count"] > len(pos["sub_attrs"]):
                errs.append((name, pn, p, "N 大于可选词条数（永假）"))

if errs:
    for e in errs:
        print("!!", e)
    raise SystemExit("自检失败，未写出文件")

# ========================================================================
# 输出
# ========================================================================
with io.open(os.path.join(OUT_DIR, "圣遗物锁定方案信息.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

names = [d["set_name"] for d in data]
with io.open(os.path.join(OUT_DIR, "settings.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump([
        {"name": "overwriteExisting", "type": "checkbox",
         "label": "覆盖已有方案（会删除重建，建议先只跑 1 套）", "default": False},
        {"name": "delayMultiplier", "type": "input-text",
         "label": "延迟系数，留空为1.2；跑全套建议填 1.4"},
        {"name": "artifactSets", "type": "multi-checkbox",
         "label": "需要配置的圣遗物套装",
         "options": ["全选"] + names,
         "default": ["角斗士的终幕礼"]},
    ], f, ensure_ascii=False, indent=2)

# manifest.json 属发布元信息，手工维护，生成器不覆盖

print("套装 %d，方案 %d" % (len(data), sum(len(d["plans"]) for d in data)))
from collections import Counter
c = Counter()
for d in data:
    for pl in d["plans"]:
        for p in pl["positions"]:
            c[(len(p["necessary_sub_attrs"]), p["min_count"])] += 1
print("(星标数, N) 分布:", dict(c))
