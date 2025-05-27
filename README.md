# Tinder for RC Pairing

- [x] Frontend scaffolded
- [ ] Backend scaffolded
- [ ] Users can add project
- [ ] Users can sort a list of projects into "want to pair" or "not interested"
- [ ] Users can easily get in touch with owners of matched projects (Zulip integration?)
- [ ] Users can be created and authenticated with RC Auth
- [ ] Projects expire at the end of the creator's batch (or just 6 weeks?)
- [ ] It's hosted somewhere accessible to RCers


## Rough Schema
Everything has an id and timestamps.

### User
- name
- email
- zuliplink


### Project
- name
- description
- expires_on datetime
- archived bool
- FK tags
- FK owner {user}

### Tags
- string (id)

### Match_Preference
- FK user
- FK project
- matched bool

### project_tags
- FK project
- FK tag
