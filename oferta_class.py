class Oferta:

    def __init__(self, url, ciudad, titulo, fecha_publicacion, empresa):
        self.provincia = None
        self.subcategoria = None
        self.categoria = None
        self.numero_vacantes = None
        self.horario = None
        self.nivel_titulacion = None
        self._id = self.url = url
        self.ciudad = ciudad
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.titulacion = None
        self.empresa = empresa
        self.salario_min = None
        self.duracion = None
        self.requisitos = None

    def to_json(self):
        oferta_json = {
            '_id': self._id,
            'ciudad': self.ciudad,
            'titulo': self.titulo,
            'fecha_publicacion': self.fecha_publicacion,
            'titulacion': self.titulacion,
            'empresa': self.empresa,
            'url': self.url,
            'nivel_titulacion': self.nivel_titulacion,
            "horario": self.horario,
            "numero_vacantes": self.numero_vacantes,
            "categoria": self.categoria,
            "subcategoria": self.subcategoria,
            "provincia": self.provincia,
            "salario_min": self.salario_min,
            "duracion": self.duracion,
            "requisitos": self.requisitos
        }
        return oferta_json
