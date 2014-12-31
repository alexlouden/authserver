Authserver
==========


# /api/user

```
{
  id: 1,
  name: "Alex",
  email: "alex@louden.com",
  roles: [
    "admin",
    "test"
  ],
  data: {
    rate_limit: 19
  }
}
```

Root:

- List  
  GET `/api/user`

- Create  
  POST `api/user`

Detail:

- Fetch  
  GET `/api/user/<id>`

- Update  
  PUT `/api/user/<id>`

- Delete  
  DELETE `/api/user/<id>`

Passwords:

- Change password  
  POST `/api/user/<id>/set_password`  
  Data: `{ password: <new_password> }`

- Check password  
  POST `/api/user/<id>/check_password`  
  Data: `{ password: <password_to_check> }`

Roles:

- Fetch user roles  
  GET `/api/user/<id>/roles`

- Check user has role  
  POST `/api/user/<id>/check_role`  
  Data: `{ name: <role_name> }`
  
- Add user role  
  POST `/api/user/<id>/add_role`  
  Data: `{ name: <role_name> }`

- Remove user role  
  POST `/api/user/<id>/remove_role`  
  Data: `{ name: <role_name> }`


Keys:

- Fetch keys  
  GET `/api/user/id/keys`

```
[
  {
    key: "key",
    secret: "secret"
  }
]
```

- Create key  
  POST `/api/user/id/create_key`  
  Data: `{ key: <new_key>, secret: <new_secret> }`


# /api/role

```
{
  count: 2,
  next: null,
  previous: null,
  results: [
    {
      id: 1,
      name: "admin"
    },
    {
      id: 2,
      name: "test"
    }
  ]
}
```

Root:

- List  
  GET `/api/role`

- Create  
  POST `api/role`

Detail: (look up via role name)

- Fetch  
  GET `/api/role/<name>`

- Update  
  PUT `/api/role/<name>`

- Delete  
  DELETE `/api/role/<name>`


# /api/key

Root:

- List  
  GET `/api/key`

```
{
  count: 1,
  next: null,
  previous: null,
  results: [
    {
      key: "key",
      secret: "secret",
      user: {
        id: 1,
        name: "Alex",
        email: "alex@louden.com",
        roles: [
          "admin",
          "test"
        ],
        data: {
          rate_limit: 19
        }
      }
    }
  ]
}
```

Detail: (look up via key)

- Fetch - GET `/api/key/<key>`

- Check secret  
  POST `/api/key/<key>/check_secret`
  Data: `{ secret: <secret> }`
