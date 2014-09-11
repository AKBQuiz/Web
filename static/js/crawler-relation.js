var relation = angular.module('relation', ['ngCookies']);
relation.controller('RelationController', ['$scope','$http','$cookies', function($scope,$http,$cookies) {
    $scope.group = [];
    $scope.grouplist = [];
    $scope.teamlist = {};
    $scope.team = [];
    $scope.memberlist = {};
    $scope.isnone = [];
    $scope.sending = false;
    $scope.success = false;
    $scope.start = 0;
    $scope.groupchange = function (i){
        var g = $scope.group[i].name
        if ($scope.teamlist[g] === undefined) {
            $http.get('/database/group_' + g + '/teamlist/?format=json').success(function(data,s,h,c){
                $scope.teamlist[g] = data;
            }).error(function(d,s,h,c){

            })
        };
        $scope.team[i] = '';
        $scope.relation[i]['member'] = '';
    };
    $scope.teamchange = function (i){
        var g = $scope.group[i].name
        var t = $scope.team[i].name
        var key =  g + t;
        if ($scope.memberlist[key] === undefined) {
            $http.get('/database/group_' + g + '/team_'+ t +'/memberlist/?format=json').success(function(data,s,h,c){
                $scope.memberlist[key] = data;
            }).error(function(d,s,h,c){

            })
        };
        $scope.relation[i]['member'] = '';
    };
    $scope.submit = function(){
        $scope.sending = true;
        var res = {};
        for (var i = 0; i < $scope.relation.length; i++) {
            var r = $scope.relation[i]
            if (r['member'] !== undefined) {
                res["rid-"+r.rid] = r['member'].mid;
            }else if($scope.isnone[i]){
                res["rid-"+r.rid] = 0;
            }
        };
        $http.post('/crawler/relation/',res,{
            xsrfHeaderName : 'X-CSRFToken',
            xsrfCookieName : 'csrftoken',
        }).success(function(data,s,h,c){
            $scope.success = true;
            $scope.sending = false;
            $scope.start -= data['num'];
            $scope.next()
        }).error(function(d,s,h,c){
            $scope.sending = false;
        })
    }

    $scope.next = function(){
        $http.get('/crawler/relation/unsolved/'+$scope.start+'-'+($scope.start+10)+'/')
        .success(function(data,s,h,c){
            $scope.relation = data;
            $scope.success = false;
            $scope.start += data.length;
        }).error(function(d,s,h,c){

        })
    }

    $http.get('/database/grouplist/?format=json').success(function(data,s,h,c){
        $scope.grouplist = data;
    }).error(function(d,s,h,c){

    })

    $scope.next()

}]);

relation.config(function($httpProvider){
   $httpProvider.defaults.transformRequest = function(obj){
     var str = [];
     for(var p in obj){
       str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
     }
     return str.join("&");
   }
   $httpProvider.defaults.headers.post = {
        'Content-Type': 'application/x-www-form-urlencoded'
   }

});
