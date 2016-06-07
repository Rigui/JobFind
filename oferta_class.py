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
        self.comunidad = None
        self.pais = None
        self.titulo = titulo
        self.fecha_publicacion = fecha_publicacion
        self.titulacion = None
        self.empresa = empresa
        self.salario_min = None
        self.duracion = None
        self.requisitos = None
        self.experiencia_min = None
        self.imprescindible = None
        self.competencias = None
        self.requirese = None
        self.nota_user = None
        self.empresas_relacionadas = None

    def to_json(self):
        oferta_json = {
            '_id': self._id,
            'ciudad': self.ciudad,
            'titulo_oferta': self.titulo,
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
            "requisitos": self.requisitos,
            "experiencia_min" : self.experiencia_min,
            "imprescindible": self.imprescindible,
            "competencias": self.competencias,
            "requirese": self.requirese,
            "comunidad": self.comunidad,
            "pais": self.pais,
            "nota_user": self.nota_user,
            "self.empresas_relacionadas": self.empresas_relacionadas
        }
        return oferta_json
