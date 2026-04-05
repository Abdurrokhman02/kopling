class WasteProcessor:
    def __init__(self):
        # Pemetaan dari label model ke kategori sampah
        self.CLASS_MAP = {
            "plastic": "anorganik",
            "botol": "anorganik",
            "kaleng": "anorganik",
            "organik": "organik",
            "sayuran": "organik",
            "buah": "organik",
            "b3": "b3",
        }
        
        self.PRIORITY = ["b3", "anorganik", "organik"]
        
    def process(self, detections):
        """
        Memproses deteksi dan mengelompokkan berdasarkan kategori.
        
        Return:
        {
            "wasteCategory": "anorganik",
            "details": [
                {"type": "botol", "qty": 2},
                {"type": "kaleng", "qty": 1}
            ],
            "jumlah": 3,
            "dominant_category": "anorganik"
        }
        """
        label_count = {}
        category_count = {
            "organik": 0,
            "anorganik": 0,
            "b3": 0
        }
        category_details = {
            "organik": [],
            "anorganik": [],
            "b3": []
        }
        
        # Hitung dan kelompokkan deteksi per label dan kategori
        for item in detections:
            label = item["label"]
            
            # Hitung per label
            label_count[label] = label_count.get(label, 0) + 1
            
            # Kategori dan pengelompokan
            category = self.CLASS_MAP.get(label, "unknown")
            if category != "unknown":
                category_count[category] += 1
                category_details[category].append(label)
        
        # Cari kategori dominan (dengan prioritas)
        dominant = None
        max_count = -1
        
        for cat in self.PRIORITY:
            if category_count[cat] > max_count:
                max_count = category_count[cat]
                dominant = cat
        
        # Buat details dengan type dan qty
        details = []
        if dominant and category_details[dominant]:
            type_count = {}
            for item_type in category_details[dominant]:
                type_count[item_type] = type_count.get(item_type, 0) + 1
            
            for item_type, qty in type_count.items():
                details.append({
                    "type": item_type,
                    "qty": qty
                })
        
        return {
            "wasteCategory": dominant if dominant else "unknown",
            "details": details,
            "jumlah": max_count if max_count > 0 else 0,
            "label_count": label_count,
            "category_count": category_count,
            "dominant_category": dominant if dominant else "unknown"
        }