var myApp = angular.module('myApp',[]);

        myApp.controller('graphicController', function($scope, $http) {

				$scope.principal = {
				    x1: 1,
                    x2: 1,
                    op: "max"
                };
				$scope.first = {
				    x1: 1,
                    x2: 1,
                    equal: 1,
                    symbol: "<="
                };
				$scope.second = {
				    x1: 1,
                    x2: 1,
                    equal: 1,
                    symbol: "<="
                };
				$scope.third = {
				    x1: 1,
                    x2: 1,
                    equal: 1,
                    symbol: "<="
                };

                $scope.restric = "";
                $scope.finalOP ="";
                $scope.text = "";
                $scope.consult = false;
                $scope.two = false;
                $scope.three = false;
                $scope.optionsSelect =  [
                  {value: '2'},
                  {value: '3'}
                ];

                $scope.finalResult = "";

                $scope.clean = function () {
                    $scope.principal = {
				        x1: 1,
                        x2: 1,
                        op: "max"
                    };
                    $scope.first = {
                        x1: 1,
                        x2: 1,
                        equal: 1,
                        symbol: "<="
                    };
                    $scope.second = {
                        x1: 1,
                        x2: 1,
                        equal: 1,
                        symbol: "<="
                    };
                    $scope.third = {
                        x1: 1,
                        x2: 1,
                        equal: 1,
                        symbol: "<="
                    };
                    $scope.text = "";
                    $scope.restric = "";
                    $scope.finalOP = "";
                    $scope.consult = false;
                    $scope.two = false;
                    $scope.three = false;
                    $scope.optionsSelect =  [
                      {value: '2'},
                      {value: '3'}
                    ];

                    $scope.finalResult = "";
                };

                $scope.changeSelect = function () {
                  if($scope.restric == "2"){
                    $scope.two = true;
                    $scope.three = false;
                  }else if($scope.restric == "3"){
                    $scope.three = true;
                    $scope.two = false;
                  }
                };

				$scope.runWith3 = function() {
				    if($scope.principal.x1 == 0 || $scope.principal.x1 == null || $scope.principal.x1 == undefined){
				        $scope.principal.x1 == 1;
                    }
                    if($scope.principal.x2 == 0 || $scope.principal.x2 == null || $scope.principal.x2 == undefined){
				        $scope.principal.x2 == 1;
                    }
                    if($scope.principal.op == "max"){
                        $scope.text = "Maximization";
                    }else{
                        $scope.text = "Minimization";
                    }

                    $http({
                        method: 'POST',
                        url: '/First',
                        data: {
                            P1: $scope.principal.x1,P2: $scope.principal.x2, P3: $scope.principal.op,
                            F1: $scope.first.x1, F2: $scope.first.x2, F3: $scope.first.equal, F4: $scope.first.symbol,
                            S1: $scope.second.x1, S2: $scope.second.x2, S3: $scope.second.equal, S4: $scope.second.symbol,
                            T1: $scope.third.x1, T2: $scope.third.x2, T3: $scope.third.equal, T4: $scope.third.symbol,
                        }

                    }).then(function (response) {
                        $scope.finalResult = response.data;
                        $scope.consult = true;
                        $scope.finalOP = ($scope.principal.x1 * $scope.finalResult.X) + ($scope.principal.x2 * $scope.finalResult.Y);
                        swal("Success", "Click on OK to check the result!", "success");
                    }, function (error) {
                        console.log(error);
                    });
                };

				$scope.runWith2 = function() {
				    if($scope.principal.x1 == 0 || $scope.principal.x1 == null || $scope.principal.x1 == undefined){
				        $scope.principal.x1 == 1;
                    }
                    if($scope.principal.x2 == 0 || $scope.principal.x2 == null || $scope.principal.x2 == undefined){
				        $scope.principal.x2 == 1;
                    }
                    if($scope.principal.op == "max"){
                        $scope.text = "Maximization";
                    }else{
                        $scope.text = "Minimization";
                    }

                    $http({
                        method: 'POST',
                        url: '/Second',
                        data: {
                            P1: $scope.principal.x1,P2: $scope.principal.x2, P3: $scope.principal.op,
                            F1: $scope.first.x1, F2: $scope.first.x2, F3: $scope.first.equal, F4: $scope.first.symbol,
                            S1: $scope.second.x1, S2: $scope.second.x2, S3: $scope.second.equal, S4: $scope.second.symbol
                        }

                    }).then(function (response) {
                        $scope.finalResult = response.data;
                        $scope.finalOP = ($scope.principal.x1 * $scope.finalResult.X) + ($scope.principal.x2 * $scope.finalResult.Y);
                        $scope.consult = true;
                        swal("Success", "Click on OK to check the result!", "success");
                    }, function (error) {
                        console.log(error);
                    });
                };



        });

