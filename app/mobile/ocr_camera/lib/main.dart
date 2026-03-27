import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

List<CameraDescription> cameras = [];

Future<void> main() async {
  // カメラの初期化
  WidgetsFlutterBinding.ensureInitialized();
  // WidgetsFlutterBinding.ensureInitialized();は、Flutterのフレームワークが完全に初期化される前に、カメラなどのプラットフォームチャネルを使用するために必要な呼び出しです。これを呼び出すことで、Flutterがネイティブコードと通信できるようになります。
  // --- 📸 利用可能なカメラを取得してグローバル変数に保存 ---
  cameras = await availableCameras();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OCR Receipt Camera',
      theme: ThemeData(
        brightness: Brightness.dark,
        primarySwatch: Colors.blue,
      ),
      home: const HomeScreen(), // 最初にIP入力画面を表示
    );
  }
}

// --- 🏠 IPアドレス入力と設定の画面 ---
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

// --- HomeScreenState の中身 ---
class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _ipController = TextEditingController(text: '192.168.1.xxx:5000');
  List<dynamic> _companies = []; // 動的に取得するリスト
  String? _selectedCode;
  bool _isLoading = false;

  // PCからリストを取得する関数
  Future<void> _fetchCompanies() async {
    setState(() { _isLoading = true; });
    try {
      final response = await http.get(
        Uri.parse('http://${_ipController.text}/companies'),
        headers: {'x-api-key': 'YOUR_SECRET_API_KEY'},
      );

      if (response.statusCode == 200) {
        // JSONをパースしてリストに入れる
        List<dynamic> data = json.decode(response.body);
        setState(() {
          _companies = data;
          _selectedCode = _companies.isNotEmpty ? _companies[0]['code'] : null;
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() { _isLoading = false; });
      print("Fetch error: $e");
    }
  }

  // 会社追加用の関数
Future<void> _addCompany(String code, String name) async {
  if (name.isEmpty) return;

  try {
    final response = await http.post(
      Uri.parse('http://${_ipController.text}/add_company'),
      headers: {
        'x-api-key': 'YOUR_SECRET_API_KEY',
        'Content-Type': 'application/json', // JSONを送ることを明示
      },
      body: json.encode({'code': code, 'name': name}),
    );
    if(response.statusCode == 200) {
        _fetchCompanies(); // 追加成功したらリストを再取得して更新
  } catch (e) {
    print("Add error: $e");
  }
}
  
// 追加用ダイアログを表示する関数
void _showAddDialog() {
  final TextEditingController _codeController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();
  showDialog(
    context: context,
    builder: (dialogcontext) => AlertDialog(
      title: const Text("新しい顧問先を追加"),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
            TextField(controller: codeController, decoration: const InputDecoration(hintText: "コード (例: 101)"), keyboardType: TextInputType.number),
            TextField(controller: nameController, decoration: const InputDecoration(hintText: "会社名")),
        ],
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(dialogcontext), child: const Text("キャンセル")),
        ElevatedButton(
          onPressed: () async{
            await _addCompany(_codeController.text, _nameController.text);
            if (!mounted) return; // 念のため、ウィジェットがまだ存在するか確認
            Navigator.pop(dialogcontext);
          },
          child: const Text("追加"),
        ),
      ],
    ),
  );
}

@override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("顧問先管理")),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            TextField(controller: _ipController, decoration: const InputDecoration(labelText: "PCのIP")),
            ElevatedButton(onPressed: _fetchCompanies, child: const Text("リスト更新")),
            const Divider(height: 40),
            if (_isLoading) const CircularProgressIndicator(),
            if (!_isLoading && _companies.isNotEmpty)
              DropdownButton<String>(
                value: _selectedCode,
                isExpanded: true,
                items: _companies.map((c) {
                  return DropdownMenuItem<String>(
                    value: c['code'],
                    child: Text("[${c['code']}] ${c['name']}"), // 👈 [101] 株式会社A と表示
                  );
                }).toList(),
                onChanged: (v) => setState(() => _selectedCode = v),
              ),
            const SizedBox(height: 10),
            ElevatedButton.icon(onPressed: _showAddDialog, icon: const Icon(Icons.add), label: const Text("会社を追加")),
            const Spacer(),
            ElevatedButton(
              onPressed: _selectedCode == null ? null : () {
                // 選択されたコードに紐づく会社名を探して渡す
                final company = _companies.firstWhere((c) => c['code'] == _selectedCode);
                Navigator.push(context, MaterialPageRoute(builder: (context) => CameraPage(
                  serverUrl: 'http://${_ipController.text}/upload',
                  apiKey: _apiKey,
                  companyName: company['name'],
                  companyCode: company['code'], // 👈 コードも渡すように追加
                )));
              },
              child: const Text("撮影開始"),
            ),
          ],
        ),
      ),
    );
  }
}

// --- 📸 OCR専用高精細カメラ画面 ---
class CameraPage extends StatefulWidget {
  final String serverUrl;
  final String apiKey;
  final String companyName;
  final String companyCode; 
  const CameraPage({super.key, required this.serverUrl, required this.apiKey, required this.companyName});

  @override
  State<CameraPage> createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  String _status = "Ready";

  @override
  void initState() {
    super.initState();
    // 背面カメラを選択
    _controller = CameraController(
      cameras.firstWhere((c) => c.lensDirection == CameraLensDirection.back),
      // --- 📸 高解像度（OCR用）を指定 ---
      ResolutionPreset.ultraHigh, // ここで最高画質（スマホの限界）を引き出す！
      enableAudio: false,
    );
    _initializeControllerFuture = _controller!.initialize();
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  // --- 📸 撮影と送信（パシャパシャ仕様） ---
  Future<void> _takeAndSendPhoto() async {
    if (_controller == null || !_controller!.value.isInitialized) return;

    try {
      setState(() { _status = "Capturing..."; });

      // 1. 静止画をキャプチャ (ビデオフレームのスクショではない)
      final image = await _controller!.takePicture();

      setState(() { _status = "Sending..."; });

      // 2. HTTP Multipart リクエストを作成
      final request = http.MultipartRequest('POST', Uri.parse(widget.serverUrl));

      // セキュリティヘッダー
      request.headers['x-api-key'] = widget.apiKey;

      request.fields['company'] = widget.companyName; // 会社名も送る
      request.fields['code'] = widget.companyCode; // 会社コードも送る

      // 画像ファイルを追加
      final file = await http.MultipartFile.fromPath(
        'photo', // Python側が request.files.get('photo') で待っているので合わせる
        image.path,
        filename: 'ocr_shot.jpg', // ファイル名は適当でOK（Python側でリネーム）
      );
      request.files.add(file);

      // 3. 送信 (バックグラウンドで行うので連写可能)
      final response = await request.send();

      // 4. 結果の処理
      if (response.statusCode == 200) {
        final timestamp = DateFormat('HH:mm:ss').format(DateTime.now());
        setState(() { _status = "✅ Sent: $timestamp"; });
        print("Photo sent successfully!");
      } else {
        setState(() { _status = "⚠️ Error: ${response.statusCode}"; });
        print("Upload failed: ${response.statusCode}");
      }

    } catch (e) {
      setState(() { _status = "⚠️ System Error: $e"; });
      print("Camera/Send error: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // プレビュー
          FutureBuilder<void>(
            future: _initializeControllerFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.done) {
                return Center(child: CameraPreview(_controller!));
              } else {
                return const Center(child: CircularProgressIndicator());
              }
            },
          ),
          
          // ステータス表示
          Positioned(
            top: 50, left: 10,
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
              decoration: BoxDecoration(color: Colors.black.withOpacity(0.5), borderRadius: BorderRadius.circular(5)),
              child: Text(_status, style: const TextStyle(color: Colors.lime, fontSize: 12)),
            ),
          ),
          
          // シャッターボタン (UI改善)
          Positioned(
            bottom: 60,
            left: 0, right: 0,
            child: Center(
              child: GestureDetector(
                onTap: _takeAndSendPhoto, // タップで撮影・送信
                child: Container(
                  width: 80, height: 80,
                  decoration: BoxDecoration(
                    color: Colors.white, shape: BoxShape.circle,
                    border: Border.all(color: Colors.grey, width: 6),
                    boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 10)],
                  ),
                ),
              ),
            ),
          ),
          
          // 戻るボタン
          Positioned(
            top: 40, right: 10,
            child: IconButton(
              icon: const Icon(Icons.close, color: Colors.white, size: 30),
              onPressed: () => Navigator.pop(context),
            ),
          ),
        ],
      ),
    );
  }
}