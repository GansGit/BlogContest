def create_blog(User,Blog,Title,Content):
    open(f"static/user/{User}/blogs/{Blog}.txt",'w').write(f"{Title}\n{Content}")
    open(f"static/Homepage-blogs/{User}.txt",'w').write(f"{Title}\n{Content}")
    return {"title":Title,"content":Content,"user":User,"blog":Blog}


