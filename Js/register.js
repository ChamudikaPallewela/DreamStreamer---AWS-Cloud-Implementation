const poolData = {
  UserPoolId: "us-east-1_h9WBxq9rE", // Replace with your Cognito User Pool ID
  ClientId: "2oo5rtbgt14k5nd9v8d117t4so", // Replace with your Cognito App Client ID
};
const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);
AWS.config.region = "us-east-1"; // Set your region

function register(event) {
  event.preventDefault(); // Prevent the form from submitting traditionally

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const dob = document.getElementById("dob").value;
  const gender = document.getElementById("gender").value; // Get the selected gender

  // Define the user attributes
  const attributeList = [];

  const dataEmail = {
    Name: "email",
    Value: email,
  };
  const attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(
    dataEmail
  );
  attributeList.push(attributeEmail);

  const dataDob = {
    Name: "birthdate",
    Value: dob,
  };
  const attributeDob = new AmazonCognitoIdentity.CognitoUserAttribute(dataDob);
  attributeList.push(attributeDob);

  const dataGender = {
    Name: "gender",
    Value: gender,
  };
  const attributeGender = new AmazonCognitoIdentity.CognitoUserAttribute(
    dataGender
  );
  attributeList.push(attributeGender);

  const dataUserType = {
    Name: "custom:UserType",
    Value: "user", // Set UserType as 'user'
  };
  const attributeUserType = new AmazonCognitoIdentity.CognitoUserAttribute(
    dataUserType
  );
  attributeList.push(attributeUserType);

  userPool.signUp(
    username,
    password,
    attributeList,
    null,
    function (err, result) {
      if (err) {
        document.getElementById("message").innerText = `Error: ${
          err.message || JSON.stringify(err)
        }`;
        console.error("Registration failed:", err);
        return;
      }

      const cognitoUser = result.user;
      document.getElementById(
        "message"
      ).innerText = `Registration successful! A verification code has been sent to your email.`;
      console.log("Registration successful:", cognitoUser.getUsername());

      // Show the verification code input field
      showVerificationCodeInput(username, email); // Pass the email directly
    }
  );
}

function showVerificationCodeInput(username, email) {
  // Pass the email here
  // Add a form for the user to input the verification code
  document.getElementById("message").innerHTML += `
        <div class="form-group mt-4">
            <label for="verificationCode">Enter Verification Code</label>
            <input type="text" class="form-control" id="verificationCode" placeholder="Enter verification code">
            <button class="btn btn-primary mt-2" onclick="verifyCode('${username}', '${email}')">Verify</button>
        </div>
    `;
}

function verifyCode(username, email) {
  // Accept email here
  const verificationCode = document.getElementById("verificationCode").value;

  const userData = {
    Username: username,
    Pool: userPool,
  };
  const cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);

  cognitoUser.confirmRegistration(
    verificationCode,
    true,
    function (err, result) {
      if (err) {
        document.getElementById("message").innerText = `Verification failed: ${
          err.message || JSON.stringify(err)
        }`;
        console.error("Verification failed:", err);
        return;
      }

      document.getElementById("message").innerText =
        "Verification successful! Sending notification...";
      console.log("Verification successful:", result);

      // Send SNS notification after successful verification
      sendSNSNotification(email); // Use email directly

      // Redirect to user.html after successful verification
      setTimeout(() => {
        window.location.href = "user.html";
      }, 2000); // 2-second delay before redirecting
    }
  );
}

function sendSNSNotification(userEmail) {
  if (userEmail) {
    console.log("User email found:", userEmail); // Add logging to confirm email

    // Include the email as a query parameter in the URL
    const url = `apiendpoint/subscribe?email=${encodeURIComponent(userEmail)}`;

    fetch(url, {
      method: "GET", // Use GET since we're sending data in the URL
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("SNS notification sent:", data);
        // Add further handling for success
      })
      .catch((error) => {
        console.error("Error sending SNS notification:", error);
        // Handle the error gracefully in the UI
      });
  } else {
    console.error("User email is not available.");
  }
}
