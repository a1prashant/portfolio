```
docker login harbour.<orgname>.com
> username: <username>
  Password: <password>
  Login Succeeded
  
docker tag <imgname>:<imgtag> harbor.<orgname>.com/<repo-name>/<imgname>:<imgtag>

docker push harbor.<orgname>.com/<repo-name>/<imgname>:<imgtag>
```
