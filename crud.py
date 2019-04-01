from flask import Flask
from flask_restful import Api, Resource, reqparse, abort



app = Flask(__name__)
api = Api(app)


USERS = {
    '1':{
        'f_name': 'Azeem',
        'l_name': 'Mian',
        'age': '27',
        'address': '993 R1'
    },
    '2':{
        'f_name': 'Abir',
        'l_name': 'Khan',
        'age': '26',
        'address': '487 Airline'
    },
    '3':{
        'f_name': 'Usman',
        'l_name': 'Ahmed',
        'age': '24',
        'address': '486 Airline'
    } 
}

# 
# parser = reqparse.RequestParser()

def user_exists(user_id):
    if user_id not in USERS:
        abort(404, message="User with id '{}' doesn't exist".format(user_id))
    return True

class UserListApi(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('f_name', type = str, required = True,
            help = 'No first name provided', location = 'json')
        self.reqparse.add_argument('l_name', type = str, required = True,
            help = 'No last name provided', location = 'json')
        self.reqparse.add_argument('age', type = int, required = True,
            help = 'No age provided', location = 'json')
        self.reqparse.add_argument('address', type = str, default = "", location = 'json')
        super(UserListApi, self).__init__()
    
    # to get list of all users
    def get(self):
        return USERS
    
    # to add/create new user
    def post(self):
        args = self.reqparse.parse_args()
        for u_id in range(1, len(USERS)):
            if u_id in USERS:
                u_id +=1

        user = {
           u_id: {
               'f_name': args['f_name'],
               'l_name': args['l_name'],
               'age': args['age'],
               'address': args['address']
           }
        }
        USERS.update(user)
        return user

class UserApi(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('f_name', type = str, location = 'json')
        self.reqparse.add_argument('l_name', type = str, location = 'json')
        self.reqparse.add_argument('age', type = int, location = 'json')
        self.reqparse.add_argument('address', type = bool, default = "", location = 'json')
        super(UserApi, self).__init__()
    
    # get user by id
    def get(self, user_id):
        if user_exists(user_id):
            return USERS[user_id]
    
    # to update user
    def put(self, user_id):
        if user_exists(user_id):
            args = self.reqparse.parse_args()
            user = {
               'f_name': args['f_name'],
               'l_name': args['l_name'],
               'age': args['age'],
               'address': args['address']
            }
            USERS[user_id] = user
            return user
    
    # to delete user
    def delete(self, user_id):
        if user_exists(user_id):
            del USERS[user_id]
            return 'User with {} id has deleted'.format(user_id)
        


api.add_resource(UserListApi, '/user', endpoint='users')
api.add_resource(UserApi, '/user/<user_id>', endpoint='user')


if __name__ == '__main__':
    app.run(debug=True)
