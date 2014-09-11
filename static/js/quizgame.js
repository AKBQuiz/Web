var timer

var appquiz = angular.module('quizapp', []);

appquiz.controller('QuizCtrl',['$scope','$http', function($scope,$http){
  var URL_PATTERN = "/quiz/api/getquiz/?group=GROUPLIST&n=20&format=json&coding=utf-8";
  $scope.grouplist = ['AKB48','SKE48','NMB48','HKT48']
  $scope.index = 0;
  $scope.correct = 0;
  $scope.incorrect = 0;
  $scope.quizlist = [{q:'  ', a:[' ','  ','   ','    '], c:0}];
  
  $scope.start = function(){
    $scope.index = 0;
    $scope.timeUsed = 0;

    var url = URL_PATTERN.
      replace('GROUPLIST', $scope.grouplist.join(','));
    $http.get(url).success(function(data) {
      $scope.quizlist = data;
      clearInterval(timer);
      timer = setInterval(function() {
          $scope.$apply(timeAdd);  
        }, 1000);
    }).error(function(data, status, headers, config){
      $scope.quizlist = [];
    });


  }
  var timeAdd = function(){
    $scope.timeUsed ++;
  }
  
  $scope.check = function(i){
    if ($scope.index >= $scope.quizlist.length - 1) {
      clearInterval(timer);
      return;
    }
    if (i == $scope.quizlist[$scope.index].c) {
      $scope.correct ++;
    }else{
      $scope.incorrect ++;
    };
    $scope.index ++;
  };
  $scope.comment={
    revise: [false,false,false,false],
    text: "",
  }
  $scope.sendcomment = function(){
    if ($scope.issending) {return};
    var id = $scope.quizlist[$scope.index];
    if (id == undefined || id == '' || id == 0){
      return;
    }else{
      $scope.comment.id = $scope.quizlist[$scope.index].id
    }
    $scope.commentecho = "正在提交...";
    $scope.issending = true;
    
    $http.post('./comment/',comment).success(function(data){
      if (data == "success") {$scope.commentecho = "提交成功！";}
      else {$scope.commentecho = "提交失败：" + data ;}
      $scope.issending = false;
    }).error(function(data, status, headers, config){
      scope.commentecho = "提交失败，请检查网络连接";
      $scope.issending = false;
    })
  };
}]);


appquiz.filter("timefilter",function(){
  return function(seconds){
    seconds = seconds || 0
    sec = seconds % 60;
    str = sec + 's'
    min = Math.floor(seconds / 60);
    if (min > 0) {
      str =  min % 60 + 'm ' + str
      hour = Math.floor(min / 60);
      if (hour > 0) {
        str =  hour + 'h ' + str
      };
    };
    return str
  }
});