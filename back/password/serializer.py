def serialize_password(item):
    title = item.title
    user = item.username
    url = item.url
    pwd = item.password
    pwd_dict = {"title": title, "user": user, "url": url, "pwd": pwd}
    return pwd_dict
