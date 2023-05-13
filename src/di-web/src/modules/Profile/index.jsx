import React, { useState } from 'react';

const ProfilePage = () => {
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    nickname: '',
    gender: ''
  });

  const [editMode, setEditMode] = useState(false);

  const handleInputChange = (event) => {
    setProfile({
      ...profile,
      [event.target.name]: event.target.value
    });
  };

  const handleEdit = () => {
    setEditMode(true);
  };

  const handleSave = () => {
    // Here you would typically send the updated profile to your server
    console.log(profile);
    setEditMode(false);
  };

  return (
    <div>
      <h1>Profile Page</h1>
      {editMode ? (
        <form>
          <label>
            Username:
            <input type="text" name="username" value={profile.username} onChange={handleInputChange} />
          </label>
          <label>
            Email:
            <input type="email" name="email" value={profile.email} onChange={handleInputChange} />
          </label>
          <label>
            Password:
            <input type="password" name="password" value={profile.password} onChange={handleInputChange} />
          </label>
          <label>
            First Name:
            <input type="text" name="firstName" value={profile.firstName} onChange={handleInputChange} />
          </label>
          <label>
            Last Name:
            <input type="text" name="lastName" value={profile.lastName} onChange={handleInputChange} />
          </label>
          <label>
            Nickname:
            <input type="text" name="nickname" value={profile.nickname} onChange={handleInputChange} />
          </label>
          <label>
            Gender:
            <select name="gender" value={profile.gender} onChange={handleInputChange}>
              <option value="">Select...</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </label>
          <button type="button" onClick={handleSave}>Save Changes</button>
        </form>
      ) : (
        <div>
          <p>Username: {profile.username}</p>
          <p>Email: {profile.email}</p>
          <p>Password: {profile.password}</p>
          <p>First Name: {profile.firstName}</p>
          <p>Last Name: {profile.lastName}</p>
          <p>Nickname: {profile.nickname}</p>
          <p>Gender: {profile.gender}</p>
          <button onClick={handleEdit}>Edit Profile</button>
        </div>
      )}
    </div>
  );
};

export default ProfilePage;
