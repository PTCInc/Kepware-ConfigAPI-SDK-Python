import re
import os

# Constants to package __init__.py to update version of package
file_location = "./kepconfig/__init__.py"
version_re_string = "([0-9]+)\.([0-9]+)\.([0-9]+(?:[ab][0-9])?)"
version_search = re.compile(r'__version__ = "'+ version_re_string + '"')
version_check = re.compile(version_re_string)

# Updates the version of package via __init__.py file
def bump_version():
    with open(file_location) as f:
        s = f.read()
    m = version_search.search(s)
    v1, v2, v3 = m.groups()
    oldv = "{0}.{1}.{2}".format(v1, v2, v3)
    
    # Need to provide version explicitly before building and releasing
    ans = input("Current version of kepconfig is: {} \nUpdate new version to? (ctrl-c to exit): ".format(oldv))
    if ans:
        m = version_check.search(ans)
        if (m==None):
            print("Version must be in format major.minor.patch (1.0.0 or 1.0.0a1) format. Exiting...")
            exit()
        newv = ans
    else:
        print("Please enter updated version number. Exiting...")
        exit()
    print("\n"+ "Updating " + file_location + " version to {}.".format(newv))
    s = s.replace(oldv, newv)
    with open(file_location, "w") as f:
        f.write(s)
    return newv


def release():
    # Update/confirm version of package
    v = bump_version()

    # Commit changes to git
    ans = input("Version updated, commit changes?(y/n)")
    if ans.lower() in ("y", "yes"):
        os.system("git add " + file_location)
        os.system('git commit -m \"{} Release\"'.format(v))
        os.system("git tag {0}".format(v))

        # This will push the committed changes and tag to Github for release
        ans = input("Change committed, push to Github server? (Y/n)")
        if ans.lower() in ("y", "yes"):
            os.system("git push --tags")
            # os.system("git push --follow-tags")

    # Build Distribution packages for external distribution
    ans = input("Build dist packages?(Y/n)")
    if ans.lower() in ("y", "yes"):
        # os.system("rm -rf dist/*") #Linux
        os.system("RMDIR /S /Q dist") #Windows
        os.system("python -m build")

    # Upload to pypi. Initially test with pypi test environment at test.pypi.org. Final release to pypi production
    # You'll be asked for credentials to authentice updating
    ans = input("Upload to pypi?(Y/n)")
    if ans.lower() in ("y", "yes"):
        ans = input("Push to production?(Y=production pypi/n=test pypi)")
        if ans.lower() in ("y", "yes"):

            #Production PyPi Server
            os.system("python -m twine upload dist/*")
        else:

            # Test PyPi Server
            os.system("python -m twine upload --repository testpypi dist/*")

        
if __name__ == "__main__":
    release()