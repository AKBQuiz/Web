var database = angular.module('Database', ['ngResource'])

database.factory('MemberInfo', ['$resource',function ($resource) {
  return $resource('/database/member_:mid/?format=json',
      {mid:'@mid'});
}]);
