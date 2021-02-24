console.log("GOOD MORNING!!");
console.log("GOOD EVENING!!");
console.log("GOOD AFTERNOON!!");

var num; 
num = 1;
console.log(num);
console.log("*********");
var num = 1;
console.log(num);

// 数値型
var num01 = 123;
var num02 = 1.23;

console.log(num01);
console.log(num02);
console.log(typeof(num01));

// 文字列型
var string_a = 'Hello';
console.log(string_a);
console.log(typeof(string_a));

// bool型
var a = 10;
var b = 1;
var bool01;
bool01 = (a > b);
console.log(bool01);
console.log(typeof(bool01));

// 配列// 配列// 配列// 配列// 配列// 配列// 配列// 配列
// Array型
var a = new Array(3);
a[0] = 'sato'
a[1] = 'arai'
a[2] = 'tanabe'
console.log(a[0]);
console.log(a[1]);
console.log(a[2]);

console.log("*********");

var a = new Array('sato', 'arai', 'tanabe');
console.log(a[0]);
console.log(a[1]);
console.log(a[2]);

console.log("*********");
console.log("*********");
// []型
var a = ['sato', 'arai', 'tanabe'];
console.log(a[0]);
console.log(a[1]);
console.log(a[2]);

console.log("*********");

var arr = ['sato', 'arai', 'tanabe'];
arr[0] = 'nakano';
console.log(arr[0]);
console.log(arr[1]);
console.log(arr[2]);

console.log("*********");
// 多次元配列
var a02 = [['sato', 'arai'], ['tanabe', 'nakano']];
console.log(a02[0][0]);
console.log(a02[0][1]);
console.log(a02[1][0]);
console.log(a02[1][1]);


console.log("*********");
console.log("*********");
// 演算子// 演算子// 演算子// 演算子// 演算子// 演算子
var x = 10;
var y = 2;

console.log(x + y);
console.log(x - y);
console.log(x * y);
console.log(x / y);
console.log(x % y);

console.log("*********");
// 関係演算子
var x = 10;
var y = 2;

console.log(x > y);
console.log(x < y);

console.log("*********");
// 論理演算子
var x = 10;
var y = 2;

console.log(x >= 5 && x <= 10);
console.log(y >= 5 && y <= 10);
console.log(x == 10 || y == 10);
console.log(x == 1 || y == 1);

// インクリメント・デクリメント
var x = 10;
var y = 2;
x++;
y--;
console.log(x);
console.log(y);

// 条件分岐// 条件分岐// 条件分岐// 条件分岐// 条件分岐// 条件分岐
var age = 22;
if (age >= 20){
    console.log('adult');
}

var age = 18;
if (age >= 20){
    console.log('adult');
}else{
    console.log('child');
}

var age = 0;
if (age >= 20){
    console.log('adult');
} else if (age == 0) {
    console.log('baby');
} else {
    console.log('child');
}

// var age = 10;
var age = 21;
// var age = 32;
// var age = 43;
// var age = 5;

if (age >= 10 && age < 20){
    console.log('10代');
} else if (age >= 20 && age < 30) {
    console.log('20代');
} else if (age >= 30 && age < 40) {
    console.log('30代');
} else {
    console.log('それ以外');
}

// 繰り返し// 繰り返し// 繰り返し// 繰り返し// 繰り返し
// for
for(var i = 0; i <= 4; i ++){
    console.log(i);
}
console.log("*********");
// break
for(var i = 0; i <= 4; i ++){
    if(i == 3){
        break;
    }
    console.log(i);
}
console.log("*********");
// continue(スキップ)
for(var i = 0; i <= 4; i ++){
    if(i == 3){
        continue;
    }
    console.log(i);
}
console.log("*********");
// for分のネスト
for(var i = 0; i <= 2; i ++){
    for(var j =0; j <= 2; j ++){
        console.log( i + '_' + j );
    }
}

var arr = [2, 4, 6, 8, 10];
var sum = 0;

for(var i = 0; i <= 4; i ++){
    sum += arr[i]
}
console.log(sum);

for(var i = 1; i <= 10; i ++){
    if(i == 3){
        continue; // ３はスキップ
    } else if(i == 7){
        break; // 7より前でbreak
    } else{
        console.log(i); // 3でも7でもない場合は、数字を表示する
    }
}

// node Greeting.js

