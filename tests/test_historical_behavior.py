"""Source-level checks where physical camera/DB hardware is unavailable."""
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]

class OriginalMethodTest(unittest.TestCase):
    def test_overwrite_same_images(self):
        m=(R/'src/python/main.py').read_text(encoding='utf-8')
        c=(R/'src/python/count_objects.py').read_text(encoding='utf-8')
        self.assertIn('cv2.imwrite(str(image_path), frame)',m)
        self.assertIn('cv2.imwrite(str(dst), image)',c)
        self.assertNotIn('.replace(',c)
        self.assertNotIn('tmp.jpg',c)

    def test_no_training_and_no_dynamic_obstacle_area(self):
        c=(R/'src/python/count_objects.py').read_text(encoding='utf-8')
        self.assertNotIn('fit(',c)
        self.assertNotIn('obstacle_detect.tflite',c)
        self.assertIn('Interpreter(model_path=str(MODEL))',c)

    def test_sql_no_new_columns_or_zero_division_patch(self):
        schema=(R/'database/schema.sql').read_text(encoding='utf-8')
        self.assertNotIn('people_count INT',schema)
        self.assertIn('previous.id + 1',schema)
        self.assertNotIn('previous.crowd_density = 0 THEN',schema)

if __name__=='__main__':unittest.main()
