# metrics.py
# 检测代理是否收敛

class SimpleMetrics:
    def __init__(self, target_state):
        """
        target_state: 目标状态(0/1)
        """
        self.target_state = target_state
        
        # 初始化
        self.convergence_step= None    # 首次收敛步数
        self.is_converged = False   # 是否收敛,开始时为false
        self.final_state = None # 最终达成共识的状态,0/1
        
        # 记录每次的状态分布
        self.step_history = []
        
    def update_metrics(self, step, agent_states):
        """更新指标"""
        # 当前的状态分布
        states = list(agent_states.values())
        count_0 = states.count(0)   # 0的个数
        count_1 = states.count(1)   # 1的个数
        total = len(states)
        
        # 历史记录
        self.step_history.append({
            'step': step,   # 步数
            'count_0': count_0, # 0的个数
            'count_1': count_1, # 1的个数
            'ratio_0': count_0 / total, # 0的占比
            'ratio_1': count_1 / total  # 1的占比
        })
        
        # 检查是否收敛
        # 只要所有状态都相同就收敛,不同就没有收敛
        if count_0 == total:  # 全部为0
            converged_state = 0
            converged = True
        elif count_1 == total:  # 全部为1
            converged_state = 1
            converged = True
        else:
            converged_state = None
            converged = False
            
        # 记录首次收敛
        # 要所有状态都相同,converged = True,
        if converged and not self.is_converged:
            self.convergence_step = step    # 收敛时的步数
            self.is_converged = True    # 收敛
            self.final_state = converged_state  # 收敛时的状态
            print(f"首次收敛! 步数: {step}, 共识状态: {converged_state}")
        
        # 更新最终共识（如果一直保持收敛）
        if converged:
            self.final_state = converged_state
        
    def get_current_stats(self):
        """获取当前状态(用于实时显示)"""
        # 历史记录为空时
        if not self.step_history:
            return "暂无数据"
            
        # 获取历史记录里的最后一步
        latest = self.step_history[-1]
        step = latest['step']
            
        status = f"步数: {step} | "
        status += f"状态0: {latest['count_0']}个 ({latest['ratio_0']:.1%}) | "
        status += f"状态1: {latest['count_1']}个 ({latest['ratio_1']:.1%})"
            
        # 显示是否收敛
        if self.is_converged:
            status += f" | 已收敛(步数{self.convergence_step})"
        else:
            status += f" | 未收敛"
            
        return status
        
    def get_final_report(self):
        """# 获取最终结果"""
        # 没有数据
        if not self.step_history:
            return "没有收集到数据"
            
        # 收敛时的总步数和最终状态
        total_steps = len(self.step_history)
        final_state = self.step_history[-1]
            
            
        report = "\n" + "="*50
        report += "\n 仿真结果报告"
        report += "\n" + "="*50
            
        # 基本信息
        report += f"\n 总仿真步数: {total_steps}"
        report += f"\n 目标状态: {self.target_state}"
            
        # 收敛情况
        if self.is_converged:
            report += f"\n 收敛状态: 已收敛"
            report += f"\n 收敛时间: {self.convergence_step} 步"
            report += f"\n 最终共识: 状态 {self.final_state}"
                
            # 准确性分析
            if self.final_state == self.target_state:
                report += f"\n 准确性: 正确 (选择了目标状态 {self.target_state})"
            else:
                report += f"\n 准确性: 错误 (选择了状态 {self.final_state}，目标是 {self.target_state})"
                
            # 效率分析
            efficiency = (total_steps - self.convergence_step) / total_steps
            report += f"\n 收敛效率: {(1-efficiency)*100:.1f}% (越快收敛效率越高)"
                
        else:
            report += f"\n 收敛状态: 未收敛"
            report += f"\n 最终分布: 状态0={final_state['count_0']}个, 状态1={final_state['count_1']}个"
                
            # 倾向分析
            if final_state['count_0'] > final_state['count_1']:
                trend = 0
                confidence = final_state['ratio_0']
            else:
                trend = 1  
                confidence = final_state['ratio_1']
                
            report += f"\n 最终倾向: 状态 {trend} (置信度: {confidence:.1%})"
                
            if trend == self.target_state:
                report += f"\n 准确性: 部分正确 (倾向目标状态但未完全收敛)"
            else:
                report += f"\n 准确性: 错误倾向"
            
        report += "\n" + "="*50
        return report