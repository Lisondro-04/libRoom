class Project {
  final String title;
  final String author;
  final String type;
  final int numberOfChapters;
  final int scenesByChapter;
  final int wordsByScene;
  final String basePath;

  Project({
    required this.title,
    required this.author,
    required this.type,
    required this.numberOfChapters,
    required this.scenesByChapter,
    required this.wordsByScene,
    required this.basePath,
  });

  Map<String, dynamic> toJson()=>{
    'title': title,
    'author': author,
    'type': type,
    'number_of_chapters': type == 'novel' ? numberOfChapters : 1,
    'scenes_by_chapter': scenesByChapter,
    'words_by_scene': wordsByScene,
    'base_path': basePath,
    'series': 'Untitled Series',
    'volume': '1',
    'license': 'CC-BY0',
    'email': 'unknow@example.com',
    };
}