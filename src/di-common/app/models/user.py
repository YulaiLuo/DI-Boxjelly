

# class User:
#     def __init__(self, username, password, email):
#         self.username = username
#         self.password = generate_password_hash(password)
#         self.email = email
#         self.created_at = datetime.utcnow()

#     def save(self):
#         mongo.db.users.insert_one({
#             'username': self.username,
#             'password': self.password,
#             'email': self.email,
#             'created_at': self.created_at
#         })

#     @staticmethod
#     def find_by_username(username):
#         user = mongo.db.users.find_one({'username': username})
#         if user:
#             return User.from_dict(user)

#     @staticmethod
#     def find_by_email(email):
#         user = mongo.db.users.find_one({'email': email})
#         if user:
#             return User.from_dict(user)

#     @staticmethod
#     def from_dict(data):
#         user = User(username=data['username'], password=data['password'], email=data['email'])
#         user.created_at = data['created_at']
#         return user