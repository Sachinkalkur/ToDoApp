from mongoengine import *
import json
import time


class User(Document):
    user_name = StringField(required=True)
    user_password = StringField(required=True)


class UserPosts(Document):
    author = ReferenceField(User)
    task_name = StringField(required=True)
    task_date = StringField(required=True)
    task_status = StringField(required=True)


def user_existence(username):
    status = True
    if not User.objects(user_name=username):
        status = False
    return status


def user_authenticate(user_data):
    status = True
    required_user = User.objects(user_name=user_data['user_name'])[0]
    if not required_user.user_password == user_data['user_password']:
        status = False
    return status


def add_user_to_database(user_data):
    new_user = User(user_name=user_data['user_name'], user_password=user_data['user_password'])
    new_user.save()


def add_posts_to_user(username, user_data):
    post_date = str(time.strftime("%H:%M:%S"))
    new_user_post = UserPosts(task_name=user_data['task_title'], task_date=post_date,
                              task_status=user_data['task_status'], author=User.objects(user_name=username)[0])
    new_user_post.save()
    user_posts = list()
    user_post = dict()
    user_post['task_name'] = new_user_post.task_name
    user_post['task_date'] = new_user_post.task_date
    user_post['task_status'] = new_user_post.task_status
    user_posts.append(user_post)
    return json.dumps(user_posts)


def edit_posts_to_user(username, user_data):
    post_date = str(time.strftime("%H:%M:%S"))
    posts = UserPosts.objects(task_name=user_data['task_title'])[0]
    posts.task_status = user_data['task_status']
    posts.task_date = post_date
    posts.save()
    user_posts = list()
    user_post = dict()
    user_post['task_name'] = posts.task_name
    user_post['task_date'] = posts.task_date
    user_post['task_status'] = posts.task_status
    user_posts.append(user_post)
    return json.dumps(user_posts)


def get_all_user_posts(username):
    user_posts = list()
    for posts in UserPosts.objects(author=User.objects(user_name=username)[0]):
        print posts.task_name, posts.task_date, posts.task_status
        user_post = dict()
        user_post['task_name'] = posts.task_name
        user_post['task_date'] = posts.task_date
        user_post['task_status'] = posts.task_status
        user_posts.append(user_post)
    json_output = json.dumps(user_posts)
    return json_output


if __name__ == '__main__':
    my_db = connect('todoapp-database')
    json_input = '{"user_password": "asdfasdf", "user_name": "sachin"}'
    json_input = json.loads(json_input)
    if not User.objects(user_name='sachin'):
        news_user = User(user_name=json_input['user_name'], user_password=json_input['user_password'])
        news_user.save()
    else:
        json_input['task_title'] = raw_input("enter task name")
        json_input['task_date'] = str(time.strftime("%H:%M:%S"))
        json_input['task_status'] = "new"
        print User.objects(user_name='sachin')[0].id
        print User.objects(user_name='sachin')[0].user_password
        new_post = UserPosts(task_name=json_input['task_title'], task_date=json_input['task_date'],
                             task_status=json_input['task_status'], author=User.objects(user_name='sachin')[0])
        new_post.save()
        print UserPosts.objects[0].task_name

        users_posts = list()
        for post in UserPosts.objects(author=User.objects(user_name='sachin')[0]):
            print post.task_name, post.task_date, post.task_status
            users_post = dict()
            users_post['task_name'] = post.task_name
            users_post['task_date'] = post.task_date
            users_post['task_status'] = post.task_status
            users_posts.append(users_post)
        print json.dumps(users_posts)

        # for posts in UserPosts.objects:
        #     posts.delete()