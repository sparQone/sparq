from modules.core.models import Model

class NicknameModel(Model):
    def save(self, data):
        # Let parent handle core fields
        super().save(data)
        
        # Handle nickname field
        if 'nickname' in data:
            print(f"Nickname module saving nickname: {data['nickname']}") 