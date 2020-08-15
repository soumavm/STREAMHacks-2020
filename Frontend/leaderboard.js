function writeUserData(userId, name) {
    firebase.database().ref('users/' + userId).set({
      username: name,
      points: 0
    });
  }