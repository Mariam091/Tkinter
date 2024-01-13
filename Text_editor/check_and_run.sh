read name
mypy $name
if [ $? -eq 0 ]; then
    # If mypy succeeds (exit status 0), run the script with Python
    echo "Type checking passed. Running the script..."
    python3 $name
else
    # If mypy fails (exit status non-zero), display an error message
    echo "Type checking failed. Please fix the type errors before running the script."
fi
