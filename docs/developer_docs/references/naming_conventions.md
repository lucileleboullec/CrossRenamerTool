# Naming Conventions
This page covers the DCC naming conventions that Cross Renamer Tool is built around - the conventions for the Python code itself are in [References: Code Style Guide](./code_style_guide.md).

## Node name structure
Most studios follow this pattern
```
{SIDE}_{description}_{IK/FK}_{SUFFIX}

# Example
L_arm_FK_ctrl
C_spine_03_jnt
R_leg_IK_grp
L_finger_index_01_bnd
```

## Sides

| Indicator | Meaning |
| --- | --- |
| `L` | Left |
| `R` | Right |
| `C` | Center |
| `M` | Mid |

## Suffixes by category

### Controls

| Suffix | Node type | 
| --- | --- |
| `ctrl` | Animator-facing control curve |

### Joints

| Suffix | Node type | 
| --- | --- |
| `jnt` | General joint |
| `bnd` | Bind joint - influences the skin |
| `twt` | Twist joint |
| `aim` | Aim constraint target join |

### Groups & Offset

| Suffix | Node type | 
| --- | --- |
| `grp` | Root group for a limb or system |
| `off` | Offset group - zero-out above a control |
| `sdk` | Set Driven Key group |
| `spc` | Space switch group |
| `null` | Generic null/zero-out group |

### Geometry

| Suffix | Node type | 
| --- | --- |
| `geo` | Final mesh |
| `hi` | High-res mesh |
| `low` | Low-res mesh |
| `pxy` | Proxy mesh |

### Helpers

| Suffix | Node type | 
| --- | --- |
| `loc` | Locator |
| `crv` | Non-control NURBS curve |
| `fol` | Follicle |
| `cls` | Cluster |
| `ikh` | IK handle |
| `bs` | Blend shape |

## Full arm example

```
L_arm_IK_grp             ← IK group, left arm
L_arm_FK_grp             ← FK group, left arm
L_arm_FK_ctrl            ← FK control, left arm
L_arm_IK_ctrl            ← IK control, left arm
 
L_shoulder_jnt           ← joint — no IK/FK on root joints
  L_elbow_jnt
    L_wrist_jnt
 
L_shoulder_bnd           ← bind joint
  L_elbow_bnd
    L_wrist_bnd
 
L_shoulder_01_twt        ← twist joint, numbered
L_shoulder_02_twt
L_elbow_01_twt
 
L_arm_geo                ← geometry
  L_arm_geoShape         ← shape
```

!!! note
    IK/FK tokens are only added when they help disambiguate - `L_shoulder_jnt` does not need one, but `L_arm_FK_ctrl` and `L_arm_IK_ctrl` do since both exist.

## Numbering
Numbers are placed at the end of the description, before the IK/FK token and suffix.
The number of digits is configurable in the **Rename** page via the **Padding** field —
the default is `3` but can be adjusted to match your studio's convention:

```
L_finger_index_01_jnt    ← padding 2
L_finger_index_001_jnt   ← padding 3 (default)
L_finger_index_0001_jnt  ← padding 4
```


## Shapes names
Shape nodes must always be named after their transform with a `Shape` suffix. The **Fix Shape Names** feature handles this automatically:

```
# ✅ Correct
L_arm_geo
    L_arm_geoShape

" ❌ Incorrect - Fix Shape Names will correct this
L_arm_geo
    pCubeShape1
```

When a transform has multiple shapes

```
L_hand_geo
    L_hand_geoShape ← index 0 - no number
    L_hand_geoShape_001 ← index 1
    L_hand_geoShape_002 ← index 2
```

## Swap L ↔ R
The **Swap L ↔ R** feature detects the side prefix and swaps it. Since the side is always first, the regex match is unambiguous:

```
L_arm_FK_ctrl → R_arm_FK_ctrl
R_leg_IK_grp → L_leg_IK_grp
C_spine_03_jnt → C_spine_03_jnt (no swap - center has no opposite)
```

Supported patterns in `constants.SWAP_SIDES`

```python
SWAP_SIDES = {
    "L": "R", 
    "l": "r", 
    "Left": "right", 
    "LEFT": "RIGHT", 
    "left": "right"
    }
```

### In `constants.py`
The suffixes and prefixes listed below are the **default presets** shipped with the tool. They reflect a common rigging convention but are fully editable from the UI - any suffix or prefix can be added, removed or reordered via the **Preset Manager** without touching the code. 

The values in `constants.py` are only used by the **Reset to defaults** action in the Preset Manager dialog.

```python
SUFFIXES = [
    "ctrl", "IK",  "FK", "jnt",
    "bnd", "twt", "aim", "grp",
    "off", "sdk", "spc", "null",
    "geo", "hi", "low", "pxy",
    "loc", "crv", "fol", "cls",
    "ikh", "bs",
]

PREFIXES = [
    "L", "R", "C", "M",
]
```



