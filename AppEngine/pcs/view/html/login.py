class LoginHtmlView (object):
    @staticmethod
    def FailureResponse(username):
        return """
<!DOCTYPE html>

<html>
  <head>
    <title>Login Failed</title>
  </head>
  
  <body>
    <h1>Login Failed</h1>
    <p>Check your username and password and try again</p>
    <form action="/login" method="POST">
      <label for="username">User ID:</label>
      <input type="text" value="%s" name="username" />
      <label for="password">Password:</label>
      <input type="password" name="password" />
      <input type="submit" />
    </form>
  </body>
</html>
        """ % (username)
        
    @staticmethod
    def SuccessResponse(session):
        return """
<!DOCTYPE html>

<html>
  <head>
    <title>Logged In</title>
  </head>
  
  <body>
    <h1>Welcome, %s</h1>
    <p><a href="%s">Make a New Reservation</a></p>
    <p><a href="%s">Manage Existing Reservations</a></p>
    <p><a href="%s">View Messages</a></p>
    <p><a href="%s">Manage Account Info</a></p>
    <p><a href="%s">Give Feedback</a></p>
  </body>
</html>
          """ % (session.name,
                 session.get_new_reservation_url(),
                 session.get_existing_reservations_url(),
                 session.get_messages_url(),
                 session.get_account_info_url(),
                 session.get_feedback_url())
    

