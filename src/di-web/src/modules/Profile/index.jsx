import React, { useEffect, useState } from "react";
import { getUserProfile, updateUserProfile } from './api';

const UserProfile = () => {
  const [userData, setUserData] = useState({
    email: "",
    first_name: "",
    last_name: "",
    nickname: "",
    gender: ""
  });
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const user_id = '645deb4a2a296fec6af44411'; // replace it with current user id after backend supports it
      const response = await getUserProfile(user_id);
      const [first_name, last_name] = response.data.name.split(' ');

      setUserData({
        email: response.data.email,
        first_name,
        last_name,
        nickname: response.data.nickname,
        gender: response.data.gender || "Not specified"
      });
    } catch (error) {
      console.log(error);
    }
  };

  const handleSaveChanges = async () => {
    const user_id = '645deb4a2a296fec6af44411'; // replace it with current user id after backend supports it

    try {
      const response = await updateUserProfile(user_id, {
        first_name: userData.first_name,
        last_name: userData.last_name,
        nickname: userData.nickname,
        gender: userData.gender,
      });

      if (response.code === 200) {
        setEditMode(false);
        fetchData();
      } else {
        console.log(response.msg);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <h1>User Profile</h1>
      {editMode ? (
        <div>
          <label>First name:</label>
          <input
            value={userData.first_name}
            onChange={(e) => setUserData({ ...userData, first_name: e.target.value })}
          />
          <label>Last name:</label>
          <input
            value={userData.last_name}
            onChange={(e) => setUserData({ ...userData, last_name: e.target.value })}
          />
          <label>Nickname:</label>
          <input
            value={userData.nickname}
            onChange={(e) =>
              setUserData({ ...userData, nickname: e.target.value })
            }
          />
          <label>Email:</label>
          <input
            value={userData.email}
            disabled
          />
          <label>Gender:</label>
          <select
            value={userData.gender}
            onChange={(e) =>
              setUserData({ ...userData, gender: e.target.value })
            }
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
          <button onClick={handleSaveChanges}>Save Changes</button>
        </div>
      ) : (
        <div>
          <p>Name: {`${userData.first_name} ${userData.last_name}`}</p>
          <p>First Name: {userData.first_name}</p>
          <p>Last Name: {userData.last_name}</p>
          <p>Nickname: {userData.nickname}</p>
          <p>Email: {userData.email}</p>
          <p>Gender: {userData.gender}</p>
          <button onClick={() => setEditMode(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
};

export default UserProfile;