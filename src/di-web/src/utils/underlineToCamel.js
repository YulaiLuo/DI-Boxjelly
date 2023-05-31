export const underlineToCamel = (variableName) => {
  return variableName.replace(/_([a-z])/g, function (match, p1) {
    return p1.toUpperCase();
  });
};

export const convertKeysToCamelCase = (obj) => {
  const camelCaseObj = {};
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      const camelCaseKey = key.replace(/_([a-z])/g, function (match, p1) {
        return p1.toUpperCase();
      });
      camelCaseObj[camelCaseKey] = obj[key];
    }
  }
  return camelCaseObj;
};
