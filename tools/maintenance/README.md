# Maintenance Utilities

`migrate_k_archive_to_l.ps1` 迁移指定的历史 FLUED 归档目录：逐文件复制到 `.partial`、计算源/目标 SHA-256、原子改名、更新可恢复清单，最后才删除已经校验的源文件。

`anonymize_mirror.py` 从主仓单向同步匿名镜像（MENTINER）：快照式历史、身份词表全量替换、内部协作文档过滤、同步前泄漏验证。

脚本默认路径是本项目 2026-07-12 的本机归档布局。其他机器必须显式传入 `-SourceRoot`、`-DestinationRoot` 和 `-LogPath`，并先检查脚本中的 `$names` 白名单。它不是通用目录同步工具。
