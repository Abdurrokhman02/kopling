class WasteProcessor:
    def __init__(self):
        self.CLASS_MAP = {
            "plastic": "anorganik"
        }
        
        self.POINTS_MAP = {
            "plastic": 5
        }
        
        self.PRIORITY = ["b3", "anorganik", "organik"]
        
    def process(self, detections):
        label_count = {}
        category_count = {
            "organik": 0,
            "anorganik": 0,
            "b3": 0
            }
        total_points = 0
        
        for item in detections:
            label = item["label"]
            
            #hitung label
            label_count[label] = label_count.get(label,0) + 1
            
            #kategori
            category = self.CLASS_MAP.get(label,"unknown")
            if category != "unknown":
                category_count[category] += 1
                
            #point
            total_points += self.POINTS_MAP.get(label, 0)
            
            
        # cari kategori dominan (dengan prioritas)
        dominant = None
        max_count = -1
        
        for cat in self.PRIORITY:
            if category_count[cat] > max_count:
                max_count = category_count[cat]
                dominant = cat
                
        return{
            "label_count": label_count,
            "category_count": category_count,
            "total_points": total_points,
            "dominant_category":dominant
        }