{
    "builds": [
      {
        "src": "studybud/wsgi.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "django_app_name/wsgi.py"
      }
    ]
}
