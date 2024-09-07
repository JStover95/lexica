flask drop-database
if [ -z "${COGNITO_USERNAME}" ]; then
    echo "Environment variable COGNITO_USERNAME not intialized. Skipping user creation."
else
    flask init-user --username ${COGNITO_USERNAME}
fi
flask init-database
