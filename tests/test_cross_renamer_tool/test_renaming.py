import unittest

from crossrenamertool.core import renamer


class TestRenaming(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(renamer.renaming("arm", 1, 3), "arm_001")

    def test_padding(self):
        self.assertEqual(renamer.renaming("arm", 1, 2), "arm_01")
        self.assertEqual(renamer.renaming("arm", 1, 4), "arm_0001")

    def test_high_number(self):
        self.assertEqual(renamer.renaming("arm", 100, 3), "arm_100")

    def test_empty_base_name(self):
        self.assertIsNone(renamer.renaming("", 1, 3))


class TestAddPrefix(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(renamer.add_prefix("arm_L", "CTRL"), "CTRL_arm_L")

    def test_empty_prefix(self):
        self.assertIsNone(renamer.add_prefix("arm_L", ""))

    def test_empty_base_name(self):
        self.assertIsNone(renamer.add_prefix("", "CTRL"))

    def test_already_has_prefix(self):
        result = renamer.add_prefix("CTRL_arm_L", "CTRL")
        self.assertEqual(result, "CTRL_CTRL_arm_L")


class TestAddSuffix(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(renamer.add_suffix("arm_L", "geo"), "arm_L_geo")

    def test_empty_suffix(self):
        self.assertIsNone(renamer.add_suffix("arm_L", ""))

    def test_empty_base_name(self):
        self.assertIsNone(renamer.add_suffix("", "geo"))


class TestSearchReplace(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            renamer.search_replace("pCube_arm_L", "pCube", "CTRL", True), "CTRL_arm_L"
        )

    def test_case_sensitive_no_match(self):
        self.assertEqual(
            renamer.search_replace("pCube_arm_L", "pcube", "CTRL", True), "pCube_arm_L"
        )

    def test_case_insensitive(self):
        self.assertEqual(
            renamer.search_replace("pCube_arm_L", "pcube", "CTRL", False), "CTRL_arm_L"
        )

    def test_no_match(self):
        self.assertEqual(renamer.search_replace("arm_L", "leg", "arm", True), "arm_L")

    def test_empty_search(self):
        result = renamer.search_replace("arm_L", "", "CTRL", True)
        self.assertEqual(result, "arm_L")

    def test_replace_with_empty(self):
        self.assertEqual(
            renamer.search_replace("pCube_arm_L", "pCube_", "", True), "arm_L"
        )

    def test_special_characters(self):
        self.assertEqual(
            renamer.search_replace("arm.L", "arm.L", "leg_L", True), "leg_L"
        )


class TestAddCharacters(unittest.TestCase):
    def test_from_start_position_0(self):
        self.assertEqual(
            renamer.add_characters("arm_L", "CTRL_", 0, True), "CTRL_arm_L"
        )

    def test_from_start_middle(self):
        self.assertEqual(renamer.add_characters("arm_L", "X", 3, True), "armX_L")

    def test_from_end_position_0(self):
        self.assertEqual(renamer.add_characters("arm_L", "_geo", 0, False), "arm_L_geo")

    def test_from_end_middle(self):
        self.assertEqual(renamer.add_characters("arm_L", "X", 1, False), "arm_XL")

    def test_empty_text(self):
        self.assertEqual(renamer.add_characters("arm_L", "", 0, True), "arm_L")


class TestRemoveCharacters(unittest.TestCase):
    def test_from_start(self):
        self.assertEqual(renamer.remove_characters("CTRL_arm_L", 0, 5, True), "arm_L")

    def test_from_end(self):
        self.assertEqual(renamer.remove_characters("arm_L", 0, 2, False), "arm")

    def test_from_start_middle(self):
        self.assertEqual(renamer.remove_characters("CTRL_arm_L", 5, 3, True), "CTRL__L")

    def test_count_zero(self):
        self.assertEqual(renamer.remove_characters("arm_L", 0, 0, True), "arm_L")

    def test_count_exceeds_length(self):
        result = renamer.remove_characters("arm", 0, 999, True)
        self.assertEqual(result, "arm")


class TestConvertCase(unittest.TestCase):
    def test_lowercase(self):
        self.assertEqual(renamer.text_to_lowercase("CTRL_ARM_L"), "ctrl_arm_l")

    def test_uppercase(self):
        self.assertEqual(renamer.text_to_uppercase("ctrl_arm_l"), "CTRL_ARM_L")

    def test_capitalize(self):
        self.assertEqual(renamer.text_to_capitalize("ctrl_arm_l"), "Ctrl_arm_l")

    def test_already_correct(self):
        self.assertEqual(renamer.text_to_lowercase("ctrl_arm_l"), "ctrl_arm_l")


class TestSwapSide(unittest.TestCase):
    SWAP_SIDES = {
        "L": "R",
        "R": "L",
        "left": "right",
        "right": "left",
        "Left": "Right",
        "Right": "Left",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT",
    }

    def test_suffix_L(self):
        self.assertEqual(renamer.swap_side("CTRL_arm_L", self.SWAP_SIDES), "CTRL_arm_R")

    def test_suffix_R(self):
        self.assertEqual(renamer.swap_side("CTRL_arm_R", self.SWAP_SIDES), "CTRL_arm_L")

    def test_prefix_L(self):
        self.assertEqual(renamer.swap_side("L_arm_ctrl", self.SWAP_SIDES), "R_arm_ctrl")

    def test_middle_L(self):
        self.assertEqual(renamer.swap_side("CTRL_L_arm", self.SWAP_SIDES), "CTRL_R_arm")

    def test_left_lowercase(self):
        self.assertEqual(renamer.swap_side("left_arm", self.SWAP_SIDES), "right_arm")

    def test_LEFT_uppercase(self):
        self.assertEqual(renamer.swap_side("LEFT_arm", self.SWAP_SIDES), "RIGHT_arm")

    def test_no_side(self):
        self.assertEqual(
            renamer.swap_side("CTRL_spine_C", self.SWAP_SIDES), "CTRL_spine_C"
        )

    def test_L_inside_word(self):
        self.assertEqual(
            renamer.swap_side("LEFTOVER_ctrl", self.SWAP_SIDES), "LEFTOVER_ctrl"
        )

    def test_empty_swap_sides(self):
        self.assertIsNone(renamer.swap_side("CTRL_arm_L", {}))


class TestFixShapeName(unittest.TestCase):
    def test_single_shape(self):
        self.assertEqual(renamer.fix_shape_name("arm_geo", 0), "arm_geoShape")

    def test_multiple_shapes(self):
        self.assertEqual(renamer.fix_shape_name("arm_geo", 1), "arm_geoShape_001")
        self.assertEqual(renamer.fix_shape_name("arm_geo", 2), "arm_geoShape_002")

    def test_already_correct(self):
        self.assertEqual(renamer.fix_shape_name("arm_geo", 0), "arm_geoShape")


class TestRenameFromParent(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(renamer.renaming("CTRL_arm_L", 1, 3), "CTRL_arm_L_001")

    def test_padding(self):
        self.assertEqual(renamer.renaming("CTRL_arm_L", 1, 2), "CTRL_arm_L_01")


if __name__ == "__main__":
    unittest.main()
