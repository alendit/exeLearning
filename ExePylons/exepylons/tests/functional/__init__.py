from exepylons import model
from hashlib import md5

# Add an admin
admin_user = model.WebUser('admin', md5('admin').hexdigest())
model.meta.Session.add(admin_user)
model.meta.Session.commit()