class User:
    """Base class for all users in the system."""
    def __init__(self, id_user, nama_lengkap, username, role):
        self.id_user = id_user
        self.nama_lengkap = nama_lengkap
        self.username = username
        self.role = role

    def get_dashboard_url(self):
        """Abstract method to get the dashboard URL endpoint."""
        raise NotImplementedError("Subclasses must implement get_dashboard_url()")

class AdminUser(User):
    """Class representing an Admin user."""
    def get_dashboard_url(self):
        # Mengembalikan nama route untuk dashboard admin yang sesungguhnya
        return 'admin.admin_dashboard_view'

class PasienUser(User):
    """Class representing a Pasien user."""
    def get_dashboard_url(self):
        # Mengembalikan nama route untuk dashboard pasien
        return 'main.dashboard'

class UserFactory:
    """Factory class to create the appropriate User object based on role."""
    @staticmethod
    def create_user(user_data):
        if not user_data:
            return None
            
        role = user_data.get('role')
        if role == 'admin':
            return AdminUser(
                id_user=user_data['id_user'],
                nama_lengkap=user_data['nama_lengkap'],
                username=user_data['username'],
                role=role
            )
        elif role == 'pasien':
            return PasienUser(
                id_user=user_data['id_user'],
                nama_lengkap=user_data['nama_lengkap'],
                username=user_data['username'],
                role=role
            )
        else:
            # Fallback for unknown roles
            return User(
                id_user=user_data.get('id_user'),
                nama_lengkap=user_data.get('nama_lengkap'),
                username=user_data.get('username'),
                role=role
            )
