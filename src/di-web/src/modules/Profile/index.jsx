import React, { useEffect, useState } from "react";
import axios from "axios";

const UserProfile = () => {
  const [userData, setUserData] = useState({
    email: "",
    name: "",
    nickname: "",
    gender: ""
  });
  const [editMode, setEditMode] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/auth/user?user_id=645deb4a2a296fec6af44411`);

      if (response.data.code === 200) {
        setUserData({
          email: response.data.data.email,
          name: response.data.data.name,
          nickname: response.data.data.nickname,
          gender: response.data.data.gender || "Not specified"
        });
      } else {
        console.log(response.data.msg);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const handleSaveChanges = async () => {
    const [first_name, last_name] = userData.name.split(' ');

    try {
      const response = await axios.put(`http://localhost:8000/auth/user?user_id=645deb4a2a296fec6af44411`, {
        first_name,
        last_name,
        nickname: userData.nickname,
        gender: userData.gender,
      });

      if (response.data.code === 200) {
        setEditMode(false);
        fetchData();
      } else {
        console.log(response.data.msg);
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
          <label>Name:</label>
          <input
            value={userData.name}
            onChange={(e) => setUserData({ ...userData, name: e.target.value })}
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
            onChange={(e) => setUserData({ ...userData, email: e.target.value })}
          />
          <label>Gender:</label>
          <input
            value={userData.gender}
            onChange={(e) =>
              setUserData({ ...userData, gender: e.target.value })
            }
          />
          <button onClick={handleSaveChanges}>Save Changes</button>
        </div>
      ) : (
        <div>
          <p>Name: {userData.name}</p>
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
