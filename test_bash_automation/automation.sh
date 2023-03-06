

#!/bin/bash

name="JohnDoe"
password="1234"

echo "Running the user-input script with the following values:"
echo "Username: $name"
echo "Password: $password"
echo ""

echo -e "$name\n$password" | ./user_input.sh


# #!/bin/bash

# name="John Doe"
# password="1234" 

# echo "Running user_input.sh with the name '$name' and password '$password'"
# echo ""

# echo "$name $password" | ./my_script.sh
