from typing import Optional


class Compatibilidad:

    @staticmethod
    def edad_es_compatible(edad_donante: int, edad_receptor: int) -> bool:
        rangos = [
            ((0, 12), (0, 18)),
            ((13, 25), (10, 40)),
            ((26, 40), (15, 55)),
            ((41, 60), (30, 70)),
            ((61, 75), (50, 80)),
            ((76, 120), (60, 120)),
        ]

        for (min_don, max_don), (min_rec, max_rec) in rangos:
            if (
                min_don <= edad_donante <= max_don
                and min_rec <= edad_receptor <= max_rec
            ):
                return True
        return False

    @staticmethod
    def sangre_es_compatible(donante: object, receptor: object) -> bool:
        compatibilidad = {
            "O-": ["O-"],
            "O+": ["O-", "O+"],
            "A-": ["O-", "A-"],
            "A+": ["O-", "O+", "A-", "A+"],
            "B-": ["O-", "B-"],
            "B+": ["O-", "O+", "B-", "B+"],
            "AB-": ["O-", "A-", "B-", "AB-"],
            "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        }
        return donante.tipo_sangre in compatibilidad.get(receptor.tipo_sangre, [])

    @staticmethod
    def organo_es_compatible(donante: object, organo_receptor: str) -> Optional[int]:
        for i, organo in enumerate(donante.organos_donante):
            if organo.nombre == organo_receptor:
                return i
        return None
