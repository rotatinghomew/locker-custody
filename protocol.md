# 车队与柜端协议

**出件资料** `parcels` 中 dimensions 是以毫米计的长、宽、高，柜格支持三个方向的正交旋转，网点和柜区按编码匹配。开柜时段为半开区间 [from, until)，until 不再允许取件。车队 `fleets` 的 zones 与 services 指定可到达的柜区和支持的方式。

**承运回执** `carrier` 字段 `fleet`、`task`、`parcel`、`revision`、`state`，case 中的任务号可用于本地联调，回执按 (fleet, task) 归属，到达次序独立于 revision。状态含 `accepted`、`not_accepted`、`cancelled_before_pickup`、`in_custody`、`deposited`、`returned`。进出库事实均带 `handoff`。deposited 提供实际 `door`、`stay`；returned 附门店接收编号。状态查询未知或接口超时不构成未接。接单、撤回、取回查询分别使用 admit、release、status 业务动作，可通过任务相关标识对账。

**柜端日志** `cabinet` 的 (door, stay) 标识一次实物占格，传输递送编号为 event，同一门的 revision 表示柜端观察顺序。`open` 只有开门事实。`occupied` 必须关联实际 `parcel` 与承运 `handoff`。`empty_after_pickup` 须带领取凭证编号 `claim`。`empty_after_abort` 由未投入的柜格确认发出，也须针对 stay。`door_fault` 表示故障不表示空。领取交接成立需匹配占格和有效领取凭证的实际取走证据。车队变更后曾拿到的本次合法交接证据仍供追溯。

**联调** `carrier` 和 `cabinet` 均为从外部摘录的消息，可逐条交给服务。交接引用由门店与对应的设备使用。一个时段相邻且无交叉的两个预留在空间上可共用柜格，前一件的实物若未清仍会阻止后一件实际投放。

交换样本为 UTF-8 NDJSON，每行独立。文件中的行顺序保留这组资料的原始提供顺序。
