class DistrictRateProvider:
    __district_to_rate = {
        'Деснянський': 25,
        'Солом\'янський': 60,
        'Дарницький': 40,
        'Голосіївський': 65,
        'Дніпровський': 35,
        'Оболонський': 55,
        'Подільський': 70,
        'Печерський': 95,
        'Святошинський': 37,
        'Шевченківський': 80,
    }

    @staticmethod
    def get_district_rate(district: str) -> int:
        return DistrictRateProvider.__district_to_rate.get(district, 0)
