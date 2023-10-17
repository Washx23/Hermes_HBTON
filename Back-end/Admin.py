"""Admin Class"""

class User:
    def __init__(self, username, password, administrator=False, email=None):
        self.username = username
        self.password = password
        self.administrator = administrator
        self.email = email
        self.products = []
        self.notes = []

    def add_products(self, product):
        self.products.append(product)

    def edit_products(self, product):
        # Implementa la lógica para editar productos
        pass

    def delete_products(self, product):
        # Implementa la lógica para eliminar productos
        pass

    def add_description(self, description):
        # Implementa la lógica para agregar una descripción
        pass


    def add_notes(self, note):
        self.notes.append(note)

    def edit_notes(self, note):
        # Implementa la lógica para editar notas
        pass

    def delete_notes(self, note):
        # Implementa la lógica para eliminar notas
        pass

    def filter_stats(self):
        # Implementa la lógica para filtrar estadísticas
        pass

    def share_campaign(self):
        # Implementa la lógica para compartir campañas
        pass
