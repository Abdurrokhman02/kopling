class WasteProcessor:
    def __init__(self):
        # Kategori yang diharapkan oleh model
        self.CATEGORIES = {"organik", "anorganik", "b3"}
        
        # Fallback mapping bila model hanya mengeluarkan tipe saja
        self.FALLBACK_MAP = {
            "plastic": "anorganik",
            "botol": "anorganik",
            "kaleng": "anorganik",
            "organik": "organik",
            "sayuran": "organik",
            "buah": "organik",
            "b3": "b3",
        }
        
    def _decode_detection(self, item):
        # Jika model sudah mengeluarkan kategori dan tipe secara terpisah
        if "category" in item and "type" in item:
            return item["category"], item["type"]

        label = item.get("label", "unknown")
        if not isinstance(label, str):
            return "unknown", "unknown"

        # Deteksi apakah label berisi tipe dan kategori, misal botol_anorganik atau anorganik_botol
        if "_" in label:
            parts = label.split("_")
            for i, part in enumerate(parts):
                if part in self.CATEGORIES:
                    other = parts[:i] + parts[i+1:]
                    return part, "_".join(other) if other else label

        # Fallback: jika label langsung kategori
        if label in self.CATEGORIES:
            return label, label

        # Fallback ke kategori dari tipe
        category = self.FALLBACK_MAP.get(label, "unknown")
        return category, label

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
            "status": "ok"
        }
        """
        label_count = {}
        category_count = {cat: 0 for cat in self.CATEGORIES}
        type_count = {}
        categories_seen = set()

        # Hitung dan kelompokkan deteksi per tipe dan kategori
        for item in detections:
            category, item_type = self._decode_detection(item)
            if category == "unknown":
                continue

            label_count[item_type] = label_count.get(item_type, 0) + 1
            type_count[item_type] = type_count.get(item_type, 0) + 1
            category_count[category] += 1
            categories_seen.add(category)

        jumlah = sum(type_count.values())
        details = [{"type": t, "qty": q} for t, q in type_count.items()]

        if jumlah == 0:
            return {
                "status": "no_waste",
                "message": "tidak ada sampah",
                "wasteCategory": "none",
                "details": [],
                "jumlah": 0,
                "label_count": label_count,
                "category_count": category_count,
                "categories_seen": []
            }

        if len(categories_seen) > 1:
            return {
                "status": "mixed_category",
                "message": "kategori berbeda",
                "wasteCategory": "mixed",
                "details": details,
                "jumlah": jumlah,
                "label_count": label_count,
                "category_count": category_count,
                "categories_seen": sorted(categories_seen)
            }

        category = categories_seen.pop()
        return {
            "status": "ok",
            "message": "sampah terdeteksi",
            "wasteCategory": category,
            "details": details,
            "jumlah": jumlah,
            "label_count": label_count,
            "category_count": category_count,
            "categories_seen": [category]
        }