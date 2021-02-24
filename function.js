function say_hello(){
    console.log('Hello World');
}

say_hello();　// 関数の実行
say_hello();
say_hello();

// 変数に関数を入れる方法
var hello = function say_hello(){
    console.log('Good Morning!');
};

hello();

var hello = function(){
    console.log('Good Morning!');
};

hello();


function say_hello02(greeting){　// 仮引数
    console.log(greeting);
};
say_hello02("GOOD MORNING!!");　// 実引数
say_hello02("GOOD AFTERNOON!!");
say_hello02("GOOD EVENING!!");

function cal(x) {
    console.log(x * 3);
};
cal(6);

function cal(x ,y ,z) {
    console.log(x * y * z);
};
cal(6, 3, 4);

// 戻り値
function cal(x, y){
    return x / y;
};
var result = cal(6, 3);　// resultという変数
console.log(result)


function cal(x ,y ,z) {
    return x + y + z;
};
var result = cal(10, 5, 8);
console.log(result);

// クラス// クラス// クラス// クラス// クラス// クラス
class Student{
    avg(math, english){
        console.log((math + english) / 2);
    }
}

var a001 = new Student();　// インスタンス化
a001.name = 'sato';
a001.avg(80, 70);

console.log(a001.name);

