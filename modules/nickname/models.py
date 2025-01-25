from modules.core.models.core import Core

class NicknameModel(Core):
    def save(self, data):
        # Let parent handle core fields
        super().save(data)
        
        # Handle nickname field
        if 'nickname' in data:
            print(f"Nickname module saving nickname: {data['nickname']}") 